# Week 7: Debugging, Properties and Persistence

Module: COMP11124 Interactive Software Design
Materials: Week 7.pdf, lab_week_6_debugging.py, main.py, tasklist.py, tasks.py, dao.py, tasks.csv

Topics covered: Debugging in VS Code, Python @property decorator, persistence using the DAO pattern with CSV and Pickle

---

## Section 1: Debugging

### Exercise 1. Finding the Problem

This exercise uses VS Code's built-in debugger to find a logical error in the Car program. The bug is not a syntax error, so the program runs fine but produces incorrect output.

lab_week_6_debugging.py:

```python
class Car:

    def __init__(self, speed:str=0) -> None:
        self.speed = speed
        self.odometer = 0
        self.time = 0

    def accelerate(self) -> None:
        self.speed += 5

    def brake(self):
        self.speed -= 5

    def step(self) -> None:
        self.odometer += self.speed
        self.time += 1

    def average_speed(self) -> float:
        return self.odometer / self.time


if __name__ == '__main__':

    my_car = Car()
    print("I'm a car!")
    while True:
        action = input("What should I do? [A]ccelerate, [B]rake, "
                        "show [O]dometer, or show average [S]peed?").upper()
        if action not in "ABOS" or len(action) != 1:
            print("I don't know how to do that")
            continue
        if action == 'A':
            my_car.accelerate()
            print("Accelerating...")
        elif action == 'B':
            my_car.brake()
            print("Braking...")
        elif action == 'O':
            print("The car has driven {} kilometers".format(my_car.odometer))
        elif action == 'S':
            print("The car's average speed was {} kph".format(my_car.average_speed()))
        my_car.step()
```

If you accelerate once, then brake twice, and check the odometer, it says 0 kilometers. That is wrong because the car should have covered some distance after accelerating.

To debug, we set a breakpoint on line 15 (self.odometer += self.speed) by clicking to the left of the line number. Then we select "Python Debugger: Debug Python File" from the dropdown next to the play button.

After accelerating, the debugger stops at the breakpoint. Expanding the self variable in the Variables panel shows odometer: 0, speed: 5, time: 0. After stepping over (executing line 15), odometer becomes 5.

We resume, brake once (speed goes to 0), then brake again. Now the Variables panel shows odometer: 5, speed: -5, time: 2. The speed has gone negative. When step() runs next, it adds -5 to the odometer, making it 0. That is the bug: braking below 0 creates a negative speed that subtracts from the odometer.

### Exercise 2. Fixing the Problem

The fix is to add a check in the brake method so speed never goes below 0:

lab_week_6_debugging.py (fixed):

```python
class Car:

    def __init__(self, speed:str=0) -> None:
        self.speed = speed
        self.odometer = 0
        self.time = 0

    def accelerate(self) -> None:
        self.speed += 5

    def brake(self):
        if self.speed >= 5:
            self.speed -= 5
        else:
            self.speed = 0

    def step(self) -> None:
        self.odometer += self.speed
        self.time += 1

    def average_speed(self) -> float:
        return self.odometer / self.time


if __name__ == '__main__':

    my_car = Car()
    print("I'm a car!")
    while True:
        action = input("What should I do? [A]ccelerate, [B]rake, "
                        "show [O]dometer, or show average [S]peed?").upper()
        if action not in "ABOS" or len(action) != 1:
            print("I don't know how to do that")
            continue
        if action == 'A':
            my_car.accelerate()
            print("Accelerating...")
        elif action == 'B':
            my_car.brake()
            print("Braking...")
        elif action == 'O':
            print("The car has driven {} kilometers".format(my_car.odometer))
        elif action == 'S':
            print("The car's average speed was {} kph".format(my_car.average_speed()))
        my_car.step()
```

Now accelerating once, braking twice, and checking the odometer shows 5 kilometers, which is correct.

### Exercise 3. Stepping Through the Code

Instead of setting breakpoints and resuming, you can step through code line by line using the debug toolbar:
- Step Over: executes the current line and moves to the next one. If the line contains a function call, it runs the entire function without entering it.
- Step Into: goes inside a function call to see what happens within it.
- Step Out: finishes the current function and returns to the caller.

### Exercise 4. Watching Variables or Expressions

The Watch panel in VS Code lets you monitor specific variables or expressions. For example, typing my_car.speed into the Watch panel shows its current value at every breakpoint. You can also watch expressions like my_car.speed > 0 which will show True or False as you step through. This is useful for tracking specific conditions without expanding the full variable tree.

---

## Section 2: Properties using the @property Decorator

Properties let you define a method that can be accessed like an attribute. This is useful when you need to compute something before returning data.

In the ToDoApp, over time we will accumulate completed tasks. But when viewing the list, we probably only care about the uncompleted ones. We could write a method uncompleted_tasks() and call it, but with @property we can access it as if it were an attribute: task_list.uncompleted_tasks instead of task_list.uncompleted_tasks().

The uncompleted_tasks property uses a list comprehension, which is a compact way to filter a list. Instead of writing a loop with append, we write a one-liner that returns a new list containing only the tasks where completed is False.

The view_tasks method is also updated: instead of showing all tasks, it only shows uncompleted ones. It uses self.tasks.index(task) to get the correct index from the full list (not the filtered one), so removal by index still works correctly.

tasklist.py:

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

    def view_tasks(self) -> None:
        print(f"Task list for {self.owner}:")
        print("The following tasks are still to be done:")
        for task in self.uncompleted_tasks:
            ix = self.tasks.index(task)
            print(f"{ix}: {task}")

    @property
    def uncompleted_tasks(self) -> list[Task]:
        return [task for task in self.tasks if not task.completed]
```

Note that in the UML diagram, uncompleted_tasks appears in the attributes section of TaskList (not the methods section) because the @property decorator makes it behave like an attribute from the outside.

---

## Section 3: Implementing Persistence

### Exercise 1. DAO (Data Access Object)

Persistence means saving the state of the program so we can load it later. The DAO pattern separates data access logic from business logic. Instead of the main function creating sample tasks directly, a DAO class handles all the reading and writing of data.

We start with a TaskTestDAO class that does not actually read from a file. It just returns hard-coded sample tasks, pretending to be a real data source. This lets us test the app structure before implementing real file I/O.

dao.py (TaskTestDAO only):

```python
from tasks import Task, RecurringTask
import datetime

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
```

The __init__ takes a storage_path parameter (could be a file path or database connection string). get_all_tasks returns all the sample tasks. save_all_tasks does nothing for now (pass).

The main module is updated: the old propagate_task_list function is removed, and two new menu choices are added for importing (loading) and exporting (saving) tasks via the DAO.

### Exercise 2. CSV Persistence

Now we implement real file persistence using CSV. The tasks.csv file looks like this:

tasks.csv:

```
title,type,date_due,completed,interval,completed_dates,date_created
Buy groceries,Task,03/03/2024,FALSE,,,07/03/2024
Do laundry,Task,09/03/2024,FALSE,,,07/03/2024
Clean room,Task,06/03/2024,FALSE,,,07/03/2024
Do homework,Task,10/03/2024,FALSE,,,07/03/2024
Walk dog,Task,12/03/2024,FALSE,,,07/03/2024
Do dishes,Task,13/03/2024,FALSE,,,07/03/2024
Go to the gym,RecurringTask,07/03/2024,FALSE,"7 days, 0:00:00","2024-02-29,2024-02-22,2024-02-14",08/02/2024
```

Each row is a task. The columns match the Task/RecurringTask attributes. RecurringTask rows have extra data in the interval and completed_dates columns.

The TaskCsvDAO class uses Python's csv module with DictReader (for reading) and DictWriter (for writing). These classes let you read/write CSV files as dictionaries where the keys are column names.

dao.py (complete with both DAO classes):

```python
from tasks import Task, RecurringTask
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
                    task = RecurringTask(task_title, datetime.datetime.strptime(task_date_due, "%Y-%m-%d"), datetime.timedelta(days=interval_days))
                    task.completed_dates = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in task_completed_dates.split(",")]
                    task.date_created = datetime.datetime.strptime(task_date_created, "%Y-%m-%d")
                else:
                    task = Task(task_title, datetime.datetime.strptime(task_date_due, "%Y-%m-%d"))
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

In get_all_tasks:
- csv.DictReader reads each row as a dictionary with column names as keys
- For each row, we check the type column to decide whether to create a Task or RecurringTask
- Dates are parsed from strings using datetime.datetime.strptime with the format "%Y-%m-%d"
- For RecurringTask, the interval string (e.g. "7 days, 0:00:00") is split to extract the number of days
- completed_dates is a comma-separated string that gets split and parsed into a list of datetime objects

In save_all_tasks:
- csv.DictWriter writes rows as dictionaries using the defined fieldnames
- isinstance(task, RecurringTask) checks if the task is a RecurringTask to handle the extra fields
- Dates are converted back to strings using strftime
- completed_dates list is joined into a comma-separated string using str.join

This is serialization: converting Python objects into a storable format (CSV strings), and deserialization: converting them back into objects when loading.

main.py:

```python
from tasklist import TaskList
from tasks import Task, RecurringTask
from dao import TaskTestDAO, TaskCsvDAO
import datetime


def main() -> None:
    task_list = TaskList("YOUR NAME")

    while True:
        print("To-Do List Manager")
        print("1. Add a task")
        print("2. View tasks")
        print("3. Remove a task")
        print("4. Edit a task")
        print("5. Complete a task")
        print("6. Import tasks")
        print("7. Export tasks")
        print("q. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter a task: ")
            input_date = input("Enter a due date (YYYY-MM-DD): ")
            date_object = datetime.datetime.strptime(input_date, "%Y-%m-%d")

            reccuring = input("Is this a reccuring task? (y/n): ")
            if reccuring == "y":
                interval = int(input("Enter the interval between each repetition (days): "))
                recurring_task = RecurringTask(title, date_object, interval=datetime.timedelta(days=int(interval)))
                task_list.add_task(recurring_task)
            else:
                task = Task(title, date_object)
                task_list.add_task(task)

        elif choice == "2":
            task_list.view_tasks()

        elif choice == "3":
            ix = int(input("Enter the index of the task to remove: "))
            try:
                task_list.get_task(ix)
            except IndexError:
                print("Invalid index.")
                continue
            task_list.remove_task(ix)

        elif choice == "4":
            ix = int(input("Enter the index of the task to edit: "))
            choice = input("What would you like to edit? (title/due date): ")

            try:
                task = task_list.get_task(ix)
            except IndexError:
                print("Invalid index.")
                continue

            if choice == "title":
                title = input("Enter a new title: ")
                task.change_title(title)
            elif choice == "due date":
                input_date = input("Enter a new due date (YYYY-MM-DD): ")
                date_object = datetime.datetime.strptime(input_date, "%Y-%m-%d")
                task.change_date_due(date_object)
            else:
                print("Invalid choice.")

        elif choice == "5":
            ix = int(input("Enter the index of the task to complete: "))

            try:
                task = task_list.get_task(ix)
            except IndexError:
                print("Invalid index.")
                continue

            task.mark_completed()

        elif choice == "6":
            task_path = input("Enter the path to the task file: ")
            dao = TaskCsvDAO(task_path)
            tasks = dao.get_all_tasks()
            for task in tasks:
                task_list.add_task(task)

        elif choice == "7":
            task_path = input("Enter the path to save the task file: ")
            dao = TaskCsvDAO(task_path)
            dao.save_all_tasks(task_list.tasks)

        elif choice == "q":
            break


if __name__ == "__main__":
    main()
```

The key changes from last week:
- The propagate_task_list function is gone. The task list starts empty.
- Choice 6 (Import) asks for a file path, creates a TaskCsvDAO, calls get_all_tasks(), and adds each task to the list
- Choice 7 (Export) asks for a save path, creates a TaskCsvDAO, and calls save_all_tasks() with the current task list
- Choices 3, 4, and 5 now use try/except IndexError to handle invalid indices gracefully instead of crashing
- The quit option is now "q" instead of "6"

### Optional Exercise 3. Serialization using Pickle

The pickle module is an alternative to CSV for persistence. It can serialize and deserialize entire Python objects without needing to manually convert each attribute to/from strings. This is much simpler than CSV when objects are complex, but the resulting files are binary (not human-readable). Note that pickle should only be used with trusted data sources as it can execute arbitrary code when loading.

The task is to implement a TaskPickleDAO class with the same get_all_tasks and save_all_tasks methods but using pickle.dump and pickle.load instead of csv.DictWriter and csv.DictReader.
