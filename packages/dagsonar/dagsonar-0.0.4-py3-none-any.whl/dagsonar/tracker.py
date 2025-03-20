import ast
import json
from pathlib import Path
from typing import Dict, List, Set, Union
from datetime import datetime

from dagsonar import (DagConfig, DagReference, ExprReference, Parser,
                      ReferenceEncoder, ShellScriptReference, TaskReference,
                      compute_hash)


class TaskTracker:
    """Main class for tracking DAG task changes."""

    def __init__(self, history_file: Path = Path("task_history.json")):
        self.history_file = history_file
        self.dag_history = self._load_history()

    def _load_history(self):
        try:
            if self.history_file.exists():
                with open(self.history_file, "r") as f:
                    return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error loading history file: {e}")

    def save_history(self, reference: List[Dict[str, str | DagReference]]):
        with open(self.history_file, "w") as f:
            json.dump(reference, f, indent=2, cls=ReferenceEncoder)

    def start_monitoring(self):
        """Start monitoring DAG tasks for changes."""
        pass

    def track_tasks(
        self, dag_configs: Dict[str, DagConfig]
    ) -> List[Dict[str, str | DagReference]]:
        dag_references: List[Dict[str, str | DagReference]] = []
        for dag, config in dag_configs.items():
            if not config.path.exists():
                print(f"Warning: Dag file not found: {config.path}")
                continue
            else:
                history = list()
                parser = Parser(config.path)
                tasks = parser.get_tasks(config.tasks)
                for task in tasks:
                    tracks = self._process_task(task, parser, src_file=config.path)
                    history.append(tracks)
                dag_references.append(
                    {
                        "dag_id": dag,
                        "reference": DagReference(dag_id=dag, task_history=history),
                    }
                )

        return dag_references
    def check_for_changes(
        self, new_reference: List[Dict[str, Union[str, DagReference]]],
        auto_save: bool = True
    ) -> List[Dict[str, str]]:
        """
        Returns a list of task IDs whose hash values have changed.
        Automatically saves the updated history if auto_save is True.
        
        Args:
            new_reference: The new references to check against history
            auto_save: Whether to automatically save the history after checking (default: True)
            
        Returns:
            List of dictionaries containing changed tasks by DAG
        """
        result = []

        for dag in new_reference:
            changed_tasks = []
            reference: DagReference = dag["reference"]

            if not isinstance(reference, DagReference):
                continue

            dag_id = reference.dag_id
            new_hashes = {task.task_id: task.hash for task in reference.task_history}
            print(dag_id, new_hashes)

            history_reference = None
            if self.dag_history is None:
                continue

            for dag in self.dag_history:
                ref = dag.get("reference")
                if ref["dag_id"] == dag_id:
                    history_reference = ref

            if history_reference is None:
                continue

            old_hashes = {
                task["task_id"]: task["hash"]
                for task in history_reference["task_history"]
            }

            for task_id, new_hash in new_hashes.items():
                if task_id not in old_hashes or old_hashes[task_id] != new_hash:
                    task_obj = next((task for task in reference.task_history if task.task_id == task_id), None)
                    
                    if task_obj:
                        timestamps = [task_obj.last_modified] + [sc.mtime for sc in task_obj.shell_scripts]
                        max_timestamp = max(timestamps)
                        
                        task_obj.last_modified = max_timestamp
                        
                        changed_tasks.append({
                            "task_id": task_id, 
                            "last_modified": max_timestamp
                        })

            result.append({"dag": reference.dag_id, "tasks": changed_tasks})
        
        if auto_save:
            self.save_history(new_reference)

        return result

    def track_changes(self, dag_configs: Dict[str, DagConfig], auto_save: bool = True) -> List[Dict[str, str]]:
        """
        Convenience method that combines tracking, checking for changes, and saving history.
        
        Args:
            dag_configs: Dictionary of DAG configurations to track
            
        Returns:
            List of dictionaries containing changed tasks by DAG
        """
        new_reference = self.track_tasks(dag_configs)
        
        changes = self.check_for_changes(new_reference, auto_save=auto_save)
        
        return changes

    def _process_task(
        self, task: ast.FunctionDef | ast.Call, parser: Parser, src_file: str = ""
    ) -> TaskReference:
        reference = TaskReference()
        if isinstance(task, ast.FunctionDef):
            reference.task_id = task.name
            reference.content = ast.dump(task)

            decorators = task.decorator_list
            decorated_bash = False
            for decorator in decorators:
                if isinstance(decorator, ast.Attribute):
                    decorated_bash = decorator.attr == "bash"

            def traverse(head, intend=0):
                # print("\t->" * intend + (ast.dump(head)))

                # Check .sh file to track
                if decorated_bash and isinstance(head, ast.Constant):
                    files = [
                        file for file in head.value.split(" ") if file.endswith(".sh")
                    ]
                    for file in files:
                        with open(file, "r") as f:
                            content = f.read()
                            reference.shell_scripts.append(
                                ShellScriptReference(
                                    path=Path(file),
                                    content=ast.dump(ast.Constant(content)),
                                    mtime=datetime.fromtimestamp(
                                        Path(file).stat().st_mtime
                                    ),
                                )
                            )

                if isinstance(head, ast.Name):
                    var = parser.find_variable_reference(variable=head)
                    if var.value is not None:
                        reference.external_variables.append(
                            ExprReference(name=head.id, content=ast.dump(var))
                        )

                if isinstance(head, ast.Call):
                    if isinstance(head.func, ast.Name):
                        fn = parser.find_function_reference(fn=head.func)
                        if fn is not None:
                            reference.called_functions.append(
                                ExprReference(name=fn.name, content=ast.dump(fn))
                            )

                for child in ast.iter_child_nodes(head):
                    traverse(child, intend + 1)

            traverse(task)
        elif isinstance(task, ast.Call):
            bash_operator = (
                isinstance(task.func, ast.Name) and task.func.id == "BashOperator"
            )

            task_id = next(
                (
                    keyword.value
                    for keyword in task.keywords
                    if keyword.arg == "task_id"
                ),
                ast.Constant,
            )
            reference.task_id = task_id.value
            reference.content = ast.dump(task)

            for arg in task.args:
                pass
            for keyword in task.keywords:
                if isinstance(keyword.value, ast.Name):
                    ref = parser.find_variable_reference(keyword.value)
                    keyword.value = ref
                    reference.external_variables.append(
                        ExprReference(
                            name=keyword.value.value, content=ast.dump(keyword)
                        )
                    )

                if (
                    bash_operator
                    and keyword.arg == "bash_command"
                    and isinstance(keyword.value, ast.Constant)
                ):
                    files = [
                        file
                        for file in keyword.value.value.split(" ")
                        if file.endswith(".sh")
                    ]
                    for file in files:
                        with open(file, "r") as f:
                            content = f.read()
                            reference.shell_scripts.append(
                                ShellScriptReference(
                                    path=Path(file),
                                    content=ast.dump(ast.Constant(content)),
                                    mtime=datetime.fromtimestamp(
                                        Path(file).stat().st_mtime
                                    ),
                                )
                            )
        reference.hash = compute_hash(reference)
        reference.last_modified = datetime.fromtimestamp(
            Path(src_file).stat().st_mtime
        )
        return reference
