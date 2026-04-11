from tasks import Task, RecurringTask
from tasklist import TaskList
from dao import TaskTestDAO, TaskCsvDAO
import datetime
from typing import Any


class TaskManagerController:

    def __init__(self, owner:str) -> None:
        self.task_list = TaskList(owner)
    
    def add_task(self, task:Task) -> None:
        self.task_list.add_task(task)

    def get_all_tasks(self) -> list[tuple[int, Task]]:
        return self.task_list.view_tasks()

    def get_uncompleted_tasks(self) -> list[Task]:
        return self.task_list.uncompleted_tasks
    
    def remove_task(self, ix:int) -> None:
        self.task_list.remove_task(ix)

    def complete_task(self, ix:int) -> None:
        self.task_list.get_task(ix).mark_completed()
    
    def save_tasks(self, path:str) -> None:
        dao = TaskCsvDAO(path)
        dao.save_all_tasks(self.task_list.tasks)
    
    def load_tasks(self, path:str) -> None:
        dao = TaskCsvDAO(path)
        tasks = dao.get_all_tasks()
        for task in tasks:
            self.task_list.add_task(task)
    