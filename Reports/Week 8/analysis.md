# Week 8: SOLID and Python Exceptions

Module: COMP11124 Object Oriented Programming
Materials: Week 8.pdf, main.py, controllers.py, ui.py, tasks.py, tasklist.py, dao.py, tasks.csv

Topics covered: SOLID Principles, Python Exceptions, Separation of Concerns in the ToDo App

---

## Section 1: SOLID Principles

### Exercise 1. Single Responsibility Principle (SRP)

The SRP states that a class should have only one reason to change. Each class should do one job. A related concept is "separation of concerns," where each part of the program addresses a separate concern, and "coupling," which is the degree of interdependence between modules. Good OO design reduces coupling.

Looking at our ToDoApp classes (without portfolio tasks):
- Task / RecurringTask: responsible for representing a task
- TaskList: responsible for managing a list of tasks
- TaskTestDAO / TaskCsvDAO: responsible for reading and writing tasks to a file

Each class has a single responsibility. But the main module violates the SRP: it handles user input, prints the menu, and calls methods of the various classes. This mixes user interface logic with business logic. We will fix this later in the lab.

### Exercise 2. Open/Closed Principle (OCP)

The OCP states that functionality should be open for extension but closed for modification. You should be able to extend a class's behaviour without modifying it, typically through inheritance and polymorphism.

In our ToDoApp, we already follow the OCP. Task is the base class with common attributes and methods, and RecurringTask extends it with recurring-specific functionality. If we wanted to add a new type of task (like a "HighPriorityTask"), we could create a new class inheriting from Task without modifying Task at all.

The same applies to the DAO classes. If we wanted to add a new type of data storage, we could create a new DAO class (like TaskPickleDAO) without modifying the existing ones. Ideally, we would have a higher-level class that all DAOs inherit from.

### Exercise 3. Liskov Substitution Principle (LSP)

The LSP states that objects of a superclass should be replaceable with objects of its subclasses without breaking the application. For example, replacing a Task object with a RecurringTask object should not cause the application to crash.

In our ToDoApp, we implement the LSP because RecurringTask inherits from Task and has the same interface in terms of attributes and methods. Although there are some functionality differences (e.g. the completed method updates the due date in RecurringTask, completed_dates tracks history), the main functionality is the same and would not directly break the application.

### Exercise 4. Interface Segregation Principle (ISP)

The ISP emphasizes that clients should not be forced to depend on interfaces they do not use. It promotes smaller, more specific interfaces tailored to the exact needs of clients.

By default, Python does not have interfaces, but we can still follow the ISP by ensuring our classes are minimal and focused on specific functionalities. For example, the Task and RecurringTask classes provide only the necessary methods for managing tasks: mark_completed() and change_date_due() for Task, and the Task class does not have methods that the recurring task does not need. An example of violating the ISP would be adding a method like "assign_standard_task_to_user" to the Task class that would not be used in RecurringTask (as it's not a standard task).

### Exercise 5. Dependency Inversion Principle (DIP)

The DIP advocates for high-level modules to depend on abstractions, not on specific details of lower-level modules. This facilitates flexibility, scalability, and ease of maintenance.

In our ToDoApp, the TaskList class interacts with tasks through the Task abstraction, allowing it to manage tasks without needing to know the specific details of each task type (whether recurring or not). Instead of accessing the stored data directly within the TaskList class, we use the DAO classes to read and write the tasks to a file. This allows us to change the way we store the tasks without needing to change the TaskList class.

---

## Section 2: Exception Handling (Optional)

Previously we looked at common errors and how to fix them. But some errors cannot be easily avoided, like opening a file that does not exist or trying to access a list index based on user input. These are called exceptions, and Python lets us handle them with try/except blocks.

The task is to add try/except blocks to the main module everywhere the get_task method is called. This catches the IndexError that is raised when the user enters an invalid index, prints a message, and asks them to try again instead of crashing. We also use try/except for file operations (FileNotFoundError).

---

## Section 3: Putting It Together for the ToDoApp

The main module still violates the SRP: it handles user input, prints the menu, and calls business logic methods. To fix this, we separate the user interface from the business logic by introducing two new classes and a factory.

The new architecture has four layers:
- CommandLineUI (ui.py): responsible for all user input and output
- TaskManagerController (controllers.py): responsible for business logic, acts as a bridge between the UI and the data/model classes
- TaskFactory (tasks.py): responsible for creating the right type of task object
- main.py: now just creates the UI and runs it

tasks.py (with TaskFactory added):

```python
import datetime
from typing import Any

class Task:
    def __init__(self, title: str, date_due: datetime.datetime):
        self.title = title
        self.date_created = datetime.datetime.now()
        self.completed = False
        self.date_due = date_due

    def change_title(self, new_title: str) -> None:
        self.title = new_title

    def change_date_due(self, date_due: datetime.datetime) -> None:
        self.date_due = date_due

    def mark_completed(self) -> None:
        self.completed = True

    def __str__(self) -> str:
        return f"{self.title} (created: {self.date_created}, due: {self.date_due}, completed: {self.completed})"


class RecurringTask(Task):
    def __init__(self, title: str, date_due: datetime.datetime, interval: datetime.timedelta):
        super().__init__(title, date_due)
        self.interval = interval
        self.completed_dates: list[datetime.datetime] = []

    def _compute_next_due_date(self) -> datetime.datetime:
        return self.date_due + self.interval

    def mark_completed(self) -> None:
        self.completed_dates.append(datetime.datetime.now())
        self.date_due = self._compute_next_due_date()

    def __str__(self) -> str:
        return f"{self.title} - Recurring (created: {self.date_created}, due: {self.date_due}, completed: {self.completed_dates}, interval: {self.interval})"


class TaskFactory:
    @staticmethod
    def create_task(title: str, date: datetime.datetime, **kwargs: Any) -> Task:
        if "interval" in kwargs:
            return RecurringTask(title, date, kwargs["interval"])
        else:
            return Task(title, date)
```

TaskFactory uses the Factory design pattern. It has a single static method create_task that decides whether to create a Task or RecurringTask based on whether the "interval" keyword argument is present. The @staticmethod decorator means it can be called without creating an instance: TaskFactory.create_task("Do homework", date) for a normal task, or TaskFactory.create_task("Go to the gym", date, interval=datetime.timedelta(days=7)) for a recurring task.

tasklist.py (with check_task_index and updated view_tasks):

```python
from tasks import Task
import datetime

class TaskList:
    def __init__(self, owner: str):
        self.owner = owner
        self.tasks: list[Task] = []

    def get_task(self, ix: int) -> Task:
        return self.tasks[ix]

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, ix: int) -> None:
        del self.tasks[ix]

    def view_tasks(self) -> list[tuple[int, Task]]:
        ix_tasks = []
        for task in self.uncompleted_tasks:
            ix = self.tasks.index(task)
            ix_tasks.append((ix, task))
        return ix_tasks

    @property
    def uncompleted_tasks(self) -> list[Task]:
        return [task for task in self.tasks if not task.completed]

    def check_task_index(self, ix: int) -> bool:
        return 0 <= ix < len(self.tasks)
```

Two changes from last week: view_tasks no longer prints anything directly. Instead it returns a list of tuples (index, task) so the UI can handle the printing. This follows the SRP: TaskList manages data, the UI handles display. check_task_index is a new method that returns True if the given index is valid, used by the controller/UI to validate before accessing.

controllers.py:

```python
from tasks import Task, RecurringTask
from tasklist import TaskList
from dao import TaskTestDAO, TaskCsvDAO
import datetime
from typing import Any


class TaskManagerController:

    def __init__(self, owner: str) -> None:
        self.task_list = TaskList(owner)

    def add_task(self, task: Task) -> None:
        self.task_list.add_task(task)

    def get_all_tasks(self) -> list[tuple[int, Task]]:
        return self.task_list.view_tasks()

    def get_uncompleted_tasks(self) -> list[Task]:
        return self.task_list.uncompleted_tasks

    def remove_task(self, ix: int) -> None:
        self.task_list.remove_task(ix)

    def complete_task(self, ix: int) -> None:
        self.task_list.get_task(ix).mark_completed()

    def save_tasks(self, path: str) -> None:
        dao = TaskCsvDAO(path)
        dao.save_all_tasks(self.task_list.tasks)

    def load_tasks(self, path: str) -> None:
        dao = TaskCsvDAO(path)
        tasks = dao.get_all_tasks()
        for task in tasks:
            self.task_list.add_task(task)
```

The controller sits between the UI and the model/data layers. It does not handle any user input or output. It creates the TaskList, delegates to it, and handles persistence through the DAO. The UI calls controller methods and the controller calls TaskList/DAO methods.

ui.py:

```python
from controllers import TaskManagerController
from tasks import TaskFactory
import datetime

class CommandLineUI:

    def _print_menu(self) -> None:
        print("To-Do List Manager")
        print("1. Add a task")
        print("2. View tasks")
        print("3. Select a task")
        print("4. Import tasks")
        print("5. Export tasks")
        print("q. Quit")

    def run(self) -> None:
        name = input("Enter your name: ")
        self.controller = TaskManagerController(name)
        load_default = input("Would you like to load a default task list? (y/n): ")
        if load_default == "y":
            self.controller.load_tasks("tasks.csv")

        while True:
            self._print_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                title = input("Enter a task: ")
                input_date = input("Enter a due date (YYYY-MM-DD): ")
                date_object = datetime.datetime.strptime(input_date, "%Y-%m-%d")

                while True:
                    reccuring = input("Is this a reccuring task? (y/n): ")
                    if reccuring == "y":
                        interval = int(input("Enter the interval between each repetition (days): "))
                        task = TaskFactory.create_task(title, date_object, interval=datetime.timedelta(days=interval))
                        break
                    elif reccuring == "n":
                        task = TaskFactory.create_task(title, date_object)
                        break
                    else:
                        print("Invalid choice.")

                self.controller.add_task(task)

            elif choice == "2":
                ix_tasks = self.controller.get_all_tasks()
                for ix, task in ix_tasks:
                    print(f"{ix} : {task}")

            elif choice == "3":
                ix = int(input("Enter the index of the task you wish to select: "))
                if self.controller.task_list.check_task_index(ix):
                    print(f"Selected task: {self.controller.task_list.get_task(ix)}")
                else:
                    print("Invalid index.")
                    continue

                while True:
                    print("1. Remove task")
                    print("2. Edit task")
                    print("3. Mark as complete")
                    print("q. Quit")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        self.controller.remove_task(ix)
                        break
                    elif choice == "2":
                        print("1. Change title")
                        print("2. Change due date")
                        choice = input("Enter your choice: ")
                        if choice == "1":
                            title = input("Enter a new title: ")
                            self.controller.task_list.get_task(ix).change_title(title)
                        elif choice == "2":
                            input_date = input("Enter a new due date (YYYY-MM-DD): ")
                            date_object = datetime.datetime.strptime(input_date, "%Y-%m-%d")
                            self.controller.task_list.get_task(ix).change_date_due(date_object)
                        else:
                            print("Invalid choice.")
                        break
                    elif choice == "3":
                        self.controller.complete_task(ix)
                        break
                    elif choice == "q":
                        break
                    else:
                        print("Invalid choice.")

            elif choice == "4":
                task_path = input("Enter the path to the task file: ")
                try:
                    self.controller.load_tasks(task_path)
                except FileNotFoundError:
                    print("File not found, please try again.")

            elif choice == "5":
                task_path = input("Enter the path to save the task file: ")
                try:
                    self.controller.save_tasks(task_path)
                except FileNotFoundError:
                    print("File not found, please try again.")

            elif choice == "q":
                break
```

CommandLineUI handles all user interaction. It creates a TaskManagerController in run() and calls its methods for everything. The menu now has a "Select a task" option (choice 3) which opens a sub-menu for removing, editing, or completing the selected task. Import/export use try/except to catch FileNotFoundError gracefully.

The _print_menu method is prefixed with _ to indicate it is a private method (only meant to be called within the class).

main.py:

```python
from ui import CommandLineUI

def main() -> None:
    ui = CommandLineUI()
    ui.run()

if __name__ == "__main__":
    main()
```

main.py is now just 4 lines. It creates the UI and runs it. All the logic that used to live here has been distributed to the appropriate classes following the SRP.

dao.py (updated to use TaskFactory):

```python
from tasks import Task, RecurringTask, TaskFactory
import datetime
import csv

class TaskTestDAO:
    def __init__(self, storage_path: str) -> None:
        self.storage_path = storage_path

    def get_all_tasks(self) -> list[Task]:
        task_list = [
            Task("Buy groceries", datetime.datetime.now() - datetime.timedelta(days=4)),
            Task("Do laundry", datetime.datetime.now() - datetime.timedelta(days=-2)),
            Task("Clean room", datetime.datetime.now() + datetime.timedelta(days=-1)),
            Task("Do homework", datetime.datetime.now() + datetime.timedelta(days=3)),
            Task("Walk dog", datetime.datetime.now() + datetime.timedelta(days=5)),
            Task("Do dishes", datetime.datetime.now() + datetime.timedelta(days=6))
        ]

        r_task = RecurringTask("Go to the gym", datetime.datetime.now(), datetime.timedelta(days=7))
        r_task.completed_dates.append(datetime.datetime.now() - datetime.timedelta(days=7))
        r_task.completed_dates.append(datetime.datetime.now() - datetime.timedelta(days=14))
        r_task.completed_dates.append(datetime.datetime.now() - datetime.timedelta(days=22))
        r_task.date_created = datetime.datetime.now() - datetime.timedelta(days=28)

        task_list.append(r_task)

        return task_list

    def save_all_tasks(self, tasks: list[Task]) -> None:
        pass


class TaskCsvDAO:
    def __init__(self, storage_path: str) -> None:
        self.storage_path = storage_path
        self.fieldnames = ["title", "type", "date_due", "completed", "interval", "completed_dates", "date_created"]

    def get_all_tasks(self) -> list[Task]:
        task_list: list[Task] = []
        with open(self.storage_path, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                task_type = row["type"]
                task_title = row["title"]
                task_date_due = row["date_due"]
                task_completed = row["completed"]
                task_interval = row["interval"]
                task_date_created = row["date_created"]
                task_completed_dates = row["completed_dates"]

                task: Task | RecurringTask

                if task_type == "RecurringTask":
                    interval_days = int(task_interval.split(" ")[0])
                    task = TaskFactory.create_task(task_title, datetime.datetime.strptime(task_date_due, "%Y-%m-%d"), interval=datetime.timedelta(days=interval_days))
                    task.completed_dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in task_completed_dates.split(",")]
                else:
                    task = TaskFactory.create_task(task_title, datetime.datetime.strptime(task_date_due, "%Y-%m-%d"))

                task.date_created = datetime.datetime.strptime(task_date_created, "%Y-%m-%d")
                task.completed = True if task_completed.lower() == "true" else False

                task_list.append(task)
        return task_list

    def save_all_tasks(self, tasks: list[Task]) -> None:
        with open(self.storage_path, "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            for task in tasks:
                row = {}

                row["title"] = task.title
                row["type"] = "RecurringTask" if isinstance(task, RecurringTask) else "Task"
                row["date_due"] = task.date_due.strftime("%Y-%m-%d")
                row["completed"] = str(task.completed)
                row["interval"] = str(task.interval) if isinstance(task, RecurringTask) else ""
                row["completed_dates"] = ",".join([date.strftime("%Y-%m-%d") for date in task.completed_dates]) if isinstance(task, RecurringTask) else ""
                row["date_created"] = task.date_created.strftime("%Y-%m-%d")
                writer.writerow(row)
```

The only change from Week 7 is that get_all_tasks now uses TaskFactory.create_task() instead of directly instantiating Task() or RecurringTask(). This follows the Factory pattern: the DAO does not need to know which specific class to create, it just passes the parameters to the factory.

tasks.csv:

```
title,type,date_due,completed,interval,completed_dates,date_created
Buy groceries,Task,2024-02-16,False,,,2024-02-20
Do laundry,Task,2024-02-22,False,,,2024-02-20
Clean room,Task,2024-02-19,False,,,2024-02-20
Do homework,Task,2024-02-23,False,,,2024-02-20
Walk dog,Task,2024-02-25,False,,,2024-02-20
Do dishes,Task,2024-02-26,False,,,2024-02-20
Go to the gym,RecurringTask,2024-02-20,False,"7 days, 0:00:00","2024-02-13,2024-02-06,2024-01-29",2024-01-23
```

The date format has been changed from DD/MM/YYYY to YYYY-MM-DD to match the strptime format used in the code.
