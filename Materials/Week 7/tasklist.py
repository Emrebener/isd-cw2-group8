from tasks import Task
import datetime

class TaskList:
    def __init__(self, owner: str):
        """Creates a new task list. This contains a list of tasks.

        Args:
            owner (str): Owner of the task list.
        """
        self.owner = owner
        self.tasks: list[Task] = []

    def get_task(self, ix: int) -> Task:
        return self.tasks[ix]

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, ix: int) -> None:
        del self.tasks[ix]

    def view_tasks(self) -> None:
        print(f"Task list for {self.owner}:")
        print("The following tasks are still to be done:")
        for task in self.uncompleted_tasks:
            # select the appropriate index for the task
            ix = self.tasks.index(task)
            print(f"{ix}: {task}")

    @property 
    def uncompleted_tasks(self) -> list[Task]:
        return [task for task in self.tasks if not task.completed]