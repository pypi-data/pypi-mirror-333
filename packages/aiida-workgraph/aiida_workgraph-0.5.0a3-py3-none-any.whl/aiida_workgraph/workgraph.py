from __future__ import annotations

import aiida.orm
import node_graph
import aiida
from node_graph.link import NodeLink
from aiida_workgraph.socket import TaskSocket
from aiida_workgraph.tasks import TaskPool
from aiida_workgraph.task import Task
import time
from aiida_workgraph.collection import TaskCollection
from aiida_workgraph.utils.graph import (
    task_deletion_hook,
    task_creation_hook,
    link_creation_hook,
    link_deletion_hook,
)
from typing import Any, Dict, List, Optional, Union

from node_graph_widget import NodeGraphWidget


class WorkGraph(node_graph.NodeGraph):
    """Build flexible workflows with AiiDA.

    The class extends from NodeGraph and provides methods to run,
    submit tasks, wait for tasks to finish, and update the process status.
    It is used to handle various states of a workgraph process and provides
    convenient operations to interact with it.

    Attributes:
        process (aiida.orm.ProcessNode): The process node that represents the process status and other details.
        state (str): The current state of the workgraph process.
        pk (int): The primary key of the process node.
    """

    NodePool = TaskPool
    platform: str = "aiida_workgraph"

    def __init__(self, name: str = "WorkGraph", **kwargs) -> None:
        """
        Initialize a WorkGraph instance.

        Args:
            name (str, optional): The name of the WorkGraph. Defaults to 'WorkGraph'.
            **kwargs: Additional keyword arguments to be passed to the WorkGraph class.
        """
        super().__init__(name, **kwargs)
        self.context = {}
        self.conditions = []
        self.process = None
        self.restart_process = None
        self.max_number_jobs = 1000000
        self.execution_count = 0
        self.max_iteration = 1000000
        self.nodes = TaskCollection(self, pool=self.NodePool)
        self.nodes.post_deletion_hooks = [task_deletion_hook]
        self.nodes.post_creation_hooks = [task_creation_hook]
        self.links.post_creation_hooks = [link_creation_hook]
        self.links.post_deletion_hooks = [link_deletion_hook]
        self._error_handlers = {}
        self._widget = NodeGraphWidget(parent=self)

    @property
    def tasks(self) -> TaskCollection:
        """Add alias to `nodes` for WorkGraph"""
        return self.nodes

    def prepare_inputs(
        self, metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        wgdata = self.to_dict()
        metadata = metadata or {}
        inputs = {"workgraph_data": wgdata, "metadata": metadata}
        return inputs

    def run(
        self,
        inputs: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Run the AiiDA workgraph process and update the process status. The method uses AiiDA's engine to run
        the process, when the process is finished, update the status of the tasks
        """
        from aiida_workgraph.engine.workgraph import WorkGraphEngine

        # set task inputs
        if inputs is not None:
            for name, input in inputs.items():
                if name not in self.tasks:
                    raise KeyError(f"Task {name} not found in WorkGraph.")
                self.tasks[name].set(input)
        # One can not run again if the process is alreay created. otherwise, a new process node will
        # be created again.
        if self.process is not None:
            print("Your workgraph is already created. Please use the submit() method.")
            return
        inputs = self.prepare_inputs(metadata=metadata)
        result, node = aiida.engine.run_get_node(WorkGraphEngine, inputs=inputs)
        self.process = node
        self.update()
        return result

    def submit(
        self,
        inputs: Optional[Dict[str, Any]] = None,
        wait: bool = False,
        timeout: int = 600,
        interval: int = 5,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> aiida.orm.ProcessNode:
        """Submit the AiiDA workgraph process and optionally wait for it to finish.
        Args:
            wait (bool): Wait for the process to finish.
            timeout (int): The maximum time in seconds to wait for the process to finish. Defaults to 600.
            restart (bool): Restart the process, and reset the modified tasks, then only re-run the modified tasks.
            new (bool): Submit a new process.
        """
        # set task inputs
        if inputs is not None:
            for name, input in inputs.items():
                if name not in self.tasks:
                    raise KeyError(f"Task {name} not found in WorkGraph.")
                self.tasks[name].set(input)

        # save the workgraph to the process node
        self.save(metadata=metadata)
        if self.process.process_state.value.upper() not in ["CREATED"]:
            raise ValueError(f"Process {self.process.pk} has already been submitted.")
        self.continue_process()
        # as long as we submit the process, it is a new submission, we should set restart_process to None
        self.restart_process = None
        if wait:
            self.wait(timeout=timeout, interval=interval)
        return self.process

    def save(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Save the udpated workgraph to the process
        This is only used for a running workgraph.
        Save the AiiDA workgraph process and update the process status.
        """
        from aiida.manage import manager
        from aiida.engine.utils import instantiate_process
        from aiida_workgraph.engine.workgraph import WorkGraphEngine

        inputs = self.prepare_inputs(metadata)
        if self.process is None:
            runner = manager.get_manager().get_runner()
            # init a process node
            process_inited = instantiate_process(runner, WorkGraphEngine, **inputs)
            process_inited.runner.persister.save_checkpoint(process_inited)
            self.process = process_inited.node
            self.process_inited = process_inited
            process_inited.close()
            print(f"WorkGraph process created, PK: {self.process.pk}")
        else:
            self.save_to_base(inputs["workgraph_data"])
        self.update()

    def save_to_base(self, wgdata: Dict[str, Any]) -> None:
        """Save new wgdata to attribute.
        It will first check the difference, and reset tasks if needed.
        """
        from aiida_workgraph.utils.analysis import WorkGraphSaver

        saver = WorkGraphSaver(
            self.process, wgdata, restart_process=self.restart_process
        )
        saver.save()

    def to_dict(self, store_nodes=False) -> Dict[str, Any]:
        from aiida_workgraph.utils import store_nodes_recursely

        wgdata = super().to_dict()
        # only alphanumeric and underscores are allowed
        wgdata["context"] = {
            key.replace(".", "__"): value for key, value in self.context.items()
        }
        wgdata.update(
            {
                "restart_process": self.restart_process.pk
                if self.restart_process
                else None,
                "max_iteration": self.max_iteration,
                "execution_count": self.execution_count,
                "conditions": self.conditions,
                "max_number_jobs": self.max_number_jobs,
            }
        )
        # save error handlers
        wgdata["error_handlers"] = self.get_error_handlers()
        wgdata["tasks"] = wgdata.pop("nodes")
        if store_nodes:
            store_nodes_recursely(wgdata)
        return wgdata

    def get_error_handlers(self) -> Dict[str, Any]:
        """Get the error handlers."""
        from aiida.engine import ExitCode

        error_handlers = {}
        for name, error_handler in self._error_handlers.items():
            error_handlers[name] = error_handler
        # convert exit code label (str) to status (int)
        for handler in error_handlers.values():
            for task in handler["tasks"].values():
                exit_codes = []
                for exit_code in task["exit_codes"]:
                    if isinstance(exit_code, int):
                        exit_codes.append(exit_code)
                    elif isinstance(exit_code, ExitCode):
                        exit_codes.append(exit_code.status)
                    else:
                        raise ValueError(
                            f"Exit code {exit_code} is not a valid exit code."
                        )
                task["exit_codes"] = exit_codes
        return error_handlers

    def wait(self, timeout: int = 600, tasks: dict = None, interval: int = 5) -> None:
        """
        Periodically checks and waits for the AiiDA workgraph process to finish until a given timeout.

        Args:
            timeout (int): The maximum time in seconds to wait for the process to finish. Defaults to 600.
            tasks (dict): Optional; specifies task states to wait for in the format {task_name: [acceptable_states]}.
            interval (int): The time interval in seconds between checks. Defaults to 5.

        Raises:
            TimeoutError: If the process does not finish within the given timeout.
        """
        terminating_states = (
            "KILLED",
            "PAUSED",
            "FINISHED",
            "FAILED",
            "CANCELLED",
            "EXCEPTED",
        )
        start = time.time()
        self.update()
        finished = False

        while not finished:
            self.update()

            if tasks is not None:
                states = []
                for name, value in tasks.items():
                    flag = self.tasks[name].state in value
                    states.append(flag)
                finished = all(states)
            else:
                finished = self.state in terminating_states

            if finished:
                print(f"Process {self.process.pk} finished with state: {self.state}")
                return

            time.sleep(interval)

            if time.time() - start > timeout:
                raise TimeoutError(
                    f"Timeout reached after {timeout} seconds while waiting for the WorkGraph: {self.process.pk}. "
                )

    def update(self) -> None:
        """
        Update the current state and primary key of the process node as well as the state, node and primary key
        of the tasks that are outgoing from the process node. This includes updating the state of process nodes
        linked to the current process, and data nodes linked to the current process.
        """
        from aiida_workgraph.utils import get_processes_latest

        if self.process is None:
            return

        self.state = self.process.process_state.value.upper()
        processes_data = get_processes_latest(self.pk)
        for name, data in processes_data.items():
            # the mapped tasks are not in the workgraph
            if name not in self.tasks:
                continue
            self.tasks[name].update_state(data)

        execution_count = getattr(self.process.outputs, "execution_count", None)
        self.execution_count = execution_count if execution_count else 0
        if self._widget is not None:
            states = {name: data["state"] for name, data in processes_data.items()}
            self._widget.states = states

    @property
    def pk(self) -> Optional[int]:
        return self.process.pk if self.process else None

    @classmethod
    def from_dict(cls, wgdata: Dict[str, Any]) -> "WorkGraph":
        from aiida_workgraph.tasks.factory.base import BaseTaskFactory

        if "tasks" in wgdata:
            wgdata["nodes"] = wgdata.pop("tasks")
        wg = super().from_dict(wgdata, class_factory=BaseTaskFactory)
        for key in [
            "max_iteration",
            "execution_count",
            "conditions",
            "max_number_jobs",
            "connectivity",
        ]:
            if key in wgdata:
                setattr(wg, key, wgdata[key])
        if "error_handlers" in wgdata:
            wg._error_handlers = wgdata["error_handlers"]
        wg.context = {
            key.replace("__", "."): value
            for key, value in wgdata.get("context", {}).items()
        }
        # for zone tasks, add their children
        for task in wg.tasks:
            if hasattr(task, "children"):
                task.children.add(wgdata["nodes"][task.name].get("children", []))
        return wg

    @classmethod
    def from_yaml(cls, filename: str = None, string: str = None) -> "WorkGraph":
        """Build WrokGraph from yaml file."""
        import yaml
        import json
        from aiida_workgraph.utils import make_json_serializable
        from node_graph.utils import yaml_to_dict
        import importlib.resources
        import jsonschema

        if filename:
            with open(filename, "r") as f:
                wgdata = yaml.safe_load(f)
        elif string:
            wgdata = yaml.safe_load(string)
        else:
            raise Exception("Please specific a filename or yaml string.")
        wgdata["nodes"] = wgdata.pop("tasks")
        wgdata = yaml_to_dict(wgdata)
        wgdata["tasks"] = wgdata.pop("nodes")
        serialized_data = make_json_serializable(wgdata)
        with importlib.resources.open_text(
            "aiida_workgraph.schemas", "aiida_workgraph.schema.json"
        ) as f:
            schema = json.load(f)
            jsonschema.validate(instance=serialized_data, schema=schema)

        nt = cls.from_dict(wgdata)
        return nt

    @classmethod
    def load(cls, pk: int | aiida.orm.ProcessNode) -> Optional["WorkGraph"]:
        """
        Load WorkGraph from the process node with the given primary key.

        Args:
            pk (int): The primary key of the process node.
        """
        from aiida_workgraph.utils import get_workgraph_data
        from aiida_workgraph.orm.workgraph import WorkGraphNode

        if isinstance(pk, int):
            process = aiida.orm.load_node(pk)
        elif isinstance(pk, aiida.orm.ProcessNode):
            process = pk
        else:
            raise ValueError(
                f"Invalid pk type: {type(pk)}, requires int or ProcessNode."
            )
        if not isinstance(process, WorkGraphNode):
            raise ValueError(f"Process {pk} is not a WorkGraph")
        wgdata = get_workgraph_data(process)
        wg = cls.from_dict(wgdata)
        wg.process = process
        wg.update()
        return wg

    def show(self) -> None:
        """
        Print the current state of the workgraph process.
        """
        from tabulate import tabulate

        table = []
        self.update()
        for task in self.tasks:
            table.append([task.name, task.pk, task.state])
        print("-" * 80)
        print("WorkGraph: {}, PK: {}, State: {}".format(self.name, self.pk, self.state))
        print("-" * 80)
        print("Tasks:")
        print(tabulate(table, headers=["Name", "PK", "State"]))
        print("-" * 80)

    # def pause(self) -> None:
    #     """Pause the workgraph."""
    #     from aiida.engine.processes import control
    #     try:
    #         control.pause_processes([self.process])
    #     except Exception as e:
    #         print(f"Pause process failed: {e}")

    def pause_tasks(self, tasks: List[str]) -> None:
        """Pause the given tasks."""
        from aiida_workgraph.utils.control import pause_tasks

        if self.process is None:
            for name in tasks:
                self.tasks[name].action = "PAUSE"
        else:
            _, msg = pause_tasks(self.process.pk, tasks)

        return "Send message to pause tasks."

    def play_tasks(self, tasks: List[str]) -> None:
        """Play the given tasks"""

        from aiida_workgraph.utils.control import play_tasks

        if self.process is None:
            for name in tasks:
                self.tasks[name].action = ""
        else:
            _, msg = play_tasks(self.process.pk, tasks)
        return "Send message to play tasks."

    def kill_tasks(self, tasks: List[str]) -> None:
        """Kill the given tasks"""

        from aiida_workgraph.utils.control import kill_tasks

        if self.process is None:
            for name in tasks:
                self.tasks[name].action = "KILL"
        else:
            _, msg = kill_tasks(self.process.pk, tasks)
        return "Send message to kill tasks."

    def continue_process(self):
        """Continue a saved process by sending the task to RabbitMA.
        Use with caution, this may launch duplicate processes."""
        from aiida.manage import get_manager

        process_controller = get_manager().get_process_controller()
        process_controller.continue_process(self.pk)

    def play(self):
        import os

        os.system("verdi process play {}".format(self.process.pk))

    def restart(self):
        """Create a restart submission."""
        if self.process is None:
            raise ValueError(
                "No process found. One can not restart from a non-existing process."
            )
        # save the current process node as restart_process
        # so that the WorkGraphSaver can compare the difference, and reset the modified tasks
        self.restart_process = self.process
        self.process = None

    def reset(self) -> None:
        """Reset the workgraph to create a new submission."""

        self.process = None
        for task in self.tasks:
            task.reset()
        self.conditions = []
        self.context = {}
        self.state = "PLANNED"

    def extend(self, wg: "WorkGraph", prefix: str = "") -> None:
        """Append a workgraph to the current workgraph.
        prefix is used to add a prefix to the task names.
        """
        for task in wg.tasks:
            task.name = prefix + task.name
            task.parent = self
            self.tasks._append(task)
        # self.conditions.extend(wg.conditions)
        self.context.update(wg.context)
        # links
        for link in wg.links:
            self.links._append(link)

    @property
    def error_handlers(self) -> Dict[str, Any]:
        """Get the error handlers."""
        return self._error_handlers

    def add_error_handler(self, handler, name, tasks: dict = None) -> None:
        """Attach an error handler to the workgraph."""
        from node_graph.executor import NodeExecutor

        self._error_handlers[name] = {
            "handler": NodeExecutor.from_callable(handler).to_dict(),
            "tasks": tasks,
        }

    def add_task(
        self, identifier: Union[str, callable], name: str = None, **kwargs
    ) -> Task:
        """Add a task to the workgraph."""
        from aiida_workgraph.decorator import build_task_from_callable
        from aiida_workgraph.tasks.factory.workgraph_task import WorkGraphTaskFactory

        if isinstance(identifier, WorkGraph):
            identifier = WorkGraphTaskFactory.create_task(identifier)
        # build the task on the fly if the identifier is a callable
        elif callable(identifier):
            identifier = build_task_from_callable(identifier)
        node = self.tasks._new(identifier, name, **kwargs)
        return node

    def add_link(self, source: TaskSocket | Task, target: TaskSocket) -> NodeLink:
        """Add a link between two tasks."""
        if isinstance(source, Task):
            source = source.outputs["_outputs"]
        link = self.links._new(source, target)
        return link

    def to_widget_value(self) -> Dict[str, Any]:
        """Convert the workgraph to a dictionary that can be used by the widget."""
        from aiida_workgraph.utils import workgraph_to_short_json, wait_to_link

        wgdata = self.to_dict()
        wait_to_link(wgdata)
        wgdata = workgraph_to_short_json(wgdata)
        return wgdata

    def _repr_mimebundle_(self, *args, **kwargs):
        # if ipywdigets > 8.0.0, use _repr_mimebundle_ instead of _ipython_display_
        self._widget.value = self.to_widget_value()
        if hasattr(self._widget, "_repr_mimebundle_"):
            return self._widget._repr_mimebundle_(*args, **kwargs)
        else:
            return self._widget._ipython_display_(*args, **kwargs)

    def to_html(self, output: str = None, **kwargs):
        """Write a standalone html file to visualize the workgraph."""
        self._widget.value = self.to_widget_value()
        return self._widget.to_html(output=output, **kwargs)

    def __repr__(self) -> str:
        return f'WorkGraph(name="{self.name}", uuid="{self.uuid}")'

    def __str__(self) -> str:
        return f'WorkGraph(name="{self.name}", uuid="{self.uuid}")'
