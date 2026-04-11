# Week 4 -- Classes and Objects

Module: COMP11124 Object Oriented Programming
Materials: Week 4.pdf, main.py, tasklist.py, tasks.py

Topics covered: Classes, Methods, Objects, Modularizing code, Documentation using docstrings and comments

---

## Exercise 1.1. Creating Classes and Initializing Objects

This is where we finally get into actual OOP. Last week's to-do list was built with plain functions -- now we convert it into a class-based design.

The lab starts with a UML diagram showing two classes: TaskList and Task. TaskList has attributes owner (a string) and tasks (a list of Task objects), plus methods add_task, remove_task, view_tasks, and list_options. Task starts simple with just a name attribute.

To define a class in Python, we use the class keyword:

```python
class TaskList:
```

Attributes are defined in the __init__ method, which is called automatically when creating a new object. The self parameter refers to the current instance of the class:

```python
class TaskList:
    def __init__(self, owner):
        self.owner = owner
        self.tasks = []
```

Now we can create objects from this class:

```python
my_task_list = TaskList("John")
print(my_task_list.owner)  # John
```

We access attributes using dot notation. Each object is its own instance, so creating TaskList("Jane") gives a separate object with its own owner and tasks.

The __init__ method can also run logic. For example, to store the owner name in uppercase:

```python
def __init__(self, owner):
    self.owner = owner.upper()
    self.tasks = []
```

---

## Exercise 1.2. Adding Methods

Methods are defined inside the class just like functions, but they always take self as the first parameter. This gives them access to the object's attributes.

The add_task method appends a task to the object's tasks list:

```python
def add_task(self, task):
    self.tasks.append(task)
```

The remove_task method deletes a task by index:

```python
def remove_task(self, ix):
    del self.tasks[ix]
```

The view_tasks method iterates over the tasks list and prints each task with its index:

```python
def view_tasks(self):
    for ix, task in enumerate(self.tasks):
        print(f"{ix}: {task}")
```

The list_options method contains the menu loop (similar to last week's while True loop) but now it lives inside the class and calls self.add_task(), self.view_tasks(), etc. instead of standalone functions.

The self parameter is crucial -- it's always a reference to the current instance of the class and is how methods access the object's attributes and other methods.

---

## Exercise 1.3. Testing the Functionality

We test the class by creating a TaskList object and manually setting some tasks:

```python
my_task_list = TaskList("YOUR NAME")
my_task_list.tasks = ["Do Homework", "Do Laundry", "Go Shopping"]
my_task_list.list_options()
```

This lets us verify that add, view, and remove all work correctly through the menu.

---

## Exercise 1.4. Composition

Composition is when one class contains objects of another class. Right now the tasks list stores plain strings, but we want to store Task objects instead.

We define the Task class with a title attribute:

```python
class Task:
    def __init__(self, title):
        self.title = title
```

Then in the list_options method, instead of adding a raw string, we create a Task object:

```python
if choice == "1":
    title = input("Enter a task: ")
    task = Task(title)
    self.add_task(task)
```

When we try to view the tasks now, we get something like "0: <__main__.Task object at 0x000001D8F63B8410>" because Python doesn't know how to display our Task object as a string. To fix this, we add the __str__ method to the Task class:

```python
def __str__(self):
    return f"Task: {self.title}"
```

The __str__ method is a special method that returns a string representation of the object. It's called automatically when you use print() on an object or convert it to a string.

The UML diagram is then expanded: the Task class gets a completed attribute (boolean, defaults to False), a mark_completed method (sets completed to True), and a change_title method (takes a new_title parameter and updates self.title). We also update __str__ to include the completed status.

The list_options method in TaskList is updated with new menu options for marking a task as completed and changing a task's title.

---

## Exercise 2.1. Adding Dates (Python Libraries)

Python libraries are collections of pre-written functions and classes. The datetime library is built into Python and lets us work with dates and times.

We import it at the top of our script:

```python
import datetime
```

We can create datetime objects in two ways:

```python
date = datetime.datetime(2021, 1, 1, 12, 0)
date = datetime.datetime.strptime("2021-01-01 12:00", "%Y-%m-%d %H:%M")
```

The strptime method parses a date string into a datetime object using a format string.

The Task class is updated with two new date attributes and a change_date_due method:

```python
def __init__(self, title, date_due):
    self.title = title
    self.date_created = datetime.datetime.now()
    self.completed = False
    self.date_due = date_due
```

date_created is set automatically to the current time using datetime.datetime.now(). date_due is passed as a parameter.

The change_date_due method works just like change_title:

```python
def change_date_due(self, date_due):
    self.date_due = date_due
```

The list_options method is updated so that when adding a task, we also ask for a due date and parse it:

```python
title = input("Enter a task: ")
input_date = input("Enter a due date (YYYY-MM-DD): ")
date_object = datetime.datetime.strptime(input_date, "%Y-%m-%d")
task = Task(title, date_object)
self.add_task(task)
```

An edit option is also added to let the user change either the title or due date of an existing task.

---

## Exercise 3.1. Modularizing Your Code -- Restructuring

Up until now, all the code was in a single file. Modularizing means splitting it into separate files (modules) to make the code easier to read, maintain, and extend.

The structure becomes:

```
ToDoApp/
    main.py
    tasks.py
    task_list.py
```

The Task class goes into tasks.py. The TaskList class goes into task_list.py, which needs to import the Task class:

```python
from tasks import Task
```

---

## Exercise 3.2. Main()

The main.py file becomes the entry point. It imports TaskList, creates an object, and runs the program:

```python
from tasklist import TaskList

def main():
    task_list = TaskList("YOUR NAME")
    task_list.list_options()

if __name__ == "__main__":
    main()
```

The if __name__ == "__main__" check ensures that main() only runs when the script is executed directly, not when it's imported as a module elsewhere.

Then the lab takes it further: the list_options method is removed from TaskList and its logic is moved into the main() function. The rationale is separation of concerns -- TaskList should only be responsible for managing tasks, not handling user interaction. The user interface (the menu loop) belongs in main.py.

After moving the code, all references to self need to be replaced with task_list (or whatever the TaskList object is called), since we're no longer inside the class.

A propagate_task_list function is also added to main.py to pre-populate the task list with sample data for testing, using datetime.timedelta to create tasks with different due dates relative to the current time.

---

## Python Files

### tasks.py

The Task class with all the functionality built up through the exercises:

```python
import datetime

class Task:
    def __init__(self, title, date_due):
        self.title = title
        self.date_created = datetime.datetime.now()
        self.completed = False
        self.date_due = date_due

    def change_title(self, new_title):
        self.title = new_title

    def change_date_due(self, date_due):
        self.date_due = date_due

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        return f"{self.title} (created: {self.date_created}, due: {self.date_due}, completed: {self.completed})"
```

The class includes type hints in the actual file (e.g. title: str, date_due: datetime.datetime) and docstrings documenting each method. The __str__ method gives a readable output when printing a Task object, showing all its attributes.

### tasklist.py

The TaskList class that manages a collection of Task objects:

```python
from tasks import Task

class TaskList:
    def __init__(self, owner):
        self.owner = owner
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, ix):
        del self.tasks[ix]

    def view_tasks(self):
        print(f"Task list for {self.owner}:")
        for ix, task in enumerate(self.tasks):
            print(f"{ix}: {task}")
```

It imports Task from tasks.py. The tasks attribute is typed as list[Task] in the actual file. The view_tasks method prints the owner's name and then each task with its index.

### main.py

The entry point that ties everything together:

```python
from tasklist import TaskList
from tasks import Task
import datetime

def propagate_task_list(task_list):
    task_list.add_task(Task("Buy groceries", datetime.datetime.now() - datetime.timedelta(days=4)))
    task_list.add_task(Task("Do laundry", datetime.datetime.now() - datetime.timedelta(days=-2)))
    task_list.add_task(Task("Clean room", datetime.datetime.now() + datetime.timedelta(days=-1)))
    task_list.add_task(Task("Do homework", datetime.datetime.now() + datetime.timedelta(days=3)))
    task_list.add_task(Task("Walk dog", datetime.datetime.now() + datetime.timedelta(days=5)))
    task_list.add_task(Task("Do dishes", datetime.datetime.now() + datetime.timedelta(days=6)))
    return task_list
```

The main() function creates a TaskList, propagates it with sample tasks, and runs a while True menu loop with 6 options: add, view, remove, edit, complete, and quit. It uses datetime.datetime.strptime to parse user-entered dates in YYYY-MM-DD format. The if __name__ == "__main__" guard at the bottom ensures main() only runs when the script is executed directly.
