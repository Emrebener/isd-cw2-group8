# Week 6: Inheritance and Polymorphism

Module: COMP11124 Interactive Software Design
Materials: Week 6.pdf, lab_week_6_debugging.py, main.py, tasklist.py, tasks.py

Topics covered: Inheritance, polymorphism, super() function, **kwargs, multiple inheritance, encapsulation, RecurringTask

---

## Section 1: Inheritance

### Exercise 1. Simple Inheritance

This exercise introduces inheritance using a Vehicle hierarchy. Inheritance lets us create new classes from existing ones, modelling an "is-a" relationship. A Car is a Vehicle, a Plane is a Vehicle, etc.

The hierarchy:

```
        Vehicle
       /       \
     Car       Plane
    /   \     /     \
Electric Petrol Propeller Jet
```

We start by defining a base Vehicle class and a Car class that inherits from it. The syntax for inheritance is class Car(Vehicle). This means Car gets all the attributes and methods of Vehicle automatically. We override the move method so cars print "driving" instead of the generic "moving".

lab_week_5.py (initial version):

```python
class Vehicle:
    def __init__(self, colour, weight, max_speed):
        self.colour = colour
        self.weight = weight
        self.max_speed = max_speed

    def move(self, speed):
        print(f"The vehicle is moving at {speed} km/h")

class Car(Vehicle):
    def move(self, speed):
        print(f"The car is driving at {speed} km/h")

generic_vehicle = Vehicle("red", 1000, 200)
generic_vehicle.move(100)

car = Car("blue", 1500, 250)
car.move(150)
```

The two move calls print different messages because Car overrides the move method from Vehicle. But Car still inherits colour, weight, and max_speed from Vehicle without us having to redefine them.

If we want to add a new attribute specific to Car (like form_factor), we need to add an __init__ method to Car. Without super(), we would have to duplicate all the parent's attribute assignments:

lab_week_5.py (Car with its own __init__, no super):

```python
class Vehicle:
    def __init__(self, colour, weight, max_speed):
        self.colour = colour
        self.weight = weight
        self.max_speed = max_speed

    def move(self, speed):
        print(f"The vehicle is moving at {speed} km/h")

class Car(Vehicle):
    def __init__(self, colour, weight, max_speed, form_factor):
        self.colour = colour
        self.weight = weight
        self.max_speed = max_speed
        self.form_factor = form_factor

    def move(self, speed):
        print(f"The car is driving at {speed} km/h")

car = Car("blue", 1500, 250, "SUV")
car.move(150)
```

This works but we have duplicated the parent's __init__ code. That is the problem super() solves.

---

### Exercise 2. super() Function

super() lets a child class call methods from its parent class. Instead of duplicating the attribute assignments, we call super().__init__() which runs the parent's __init__ and only add what is new in the child:

lab_week_5.py (with super):

```python
class Vehicle:
    def __init__(self, colour, weight, max_speed):
        self.colour = colour
        self.weight = weight
        self.max_speed = max_speed

    def move(self, speed):
        print(f"The vehicle is moving at {speed} km/h")

class Car(Vehicle):
    def __init__(self, colour, weight, max_speed, form_factor):
        super().__init__(colour, weight, max_speed)
        self.form_factor = form_factor

    def move(self, speed):
        print(f"The car is driving at {speed} km/h")

class Electric(Car):
    def __init__(self, colour, weight, max_speed, form_factor, battery_capacity):
        super().__init__(colour, weight, max_speed, form_factor)
        self.battery_capacity = battery_capacity

    def move(self, speed):
        print(f"The electric car is driving at {speed} km/h")

class Petrol(Car):
    def __init__(self, colour, weight, max_speed, form_factor, fuel_capacity):
        super().__init__(colour, weight, max_speed, form_factor)
        self.fuel_capacity = fuel_capacity

    def move(self, speed):
        print(f"The petrol car is driving at {speed} km/h")

electric_car = Electric("green", 1200, 200, "Hatchback", 100)
electric_car.move(100)

petrol_car = Petrol("red", 1500, 250, "SUV", 50)
petrol_car.move(150)

generic_vehicle = Vehicle("red", 1000, 200)
generic_vehicle.move(100)
```

Each class only defines what is unique to it and delegates the rest to the parent via super(). The chain goes Electric -> Car -> Vehicle, each level adding its own attribute.

Now suppose we want to add max_range to both Electric and Petrol. Instead of adding it to each child class separately, we think about the hierarchy: all vehicles could have a max range. So we add it to Vehicle as an optional parameter (defaulting to None), and it flows down to all children automatically:

lab_week_5.py (with max_range on Vehicle):

```python
class Vehicle:
    def __init__(self, colour, weight, max_speed, max_range=None):
        self.colour = colour
        self.weight = weight
        self.max_speed = max_speed
        self.max_range = max_range

    def move(self, speed):
        print(f"The vehicle is moving at {speed} km/h")

class Car(Vehicle):
    def __init__(self, colour, weight, max_speed, form_factor, max_range=None):
        super().__init__(colour, weight, max_speed, max_range)
        self.form_factor = form_factor

    def move(self, speed):
        print(f"The car is driving at {speed} km/h")

class Electric(Car):
    def __init__(self, colour, weight, max_speed, form_factor, battery_capacity, max_range=None):
        super().__init__(colour, weight, max_speed, form_factor, max_range)
        self.battery_capacity = battery_capacity

    def move(self, speed):
        print(f"The electric car is driving at {speed} km/h and has a maximum range of {self.max_range} km")

class Petrol(Car):
    def __init__(self, colour, weight, max_speed, form_factor, fuel_capacity, max_range=None):
        super().__init__(colour, weight, max_speed, form_factor, max_range)
        self.fuel_capacity = fuel_capacity

    def move(self, speed):
        print(f"The petrol car is driving at {speed} km/h")
```

This works but adding each new optional attribute means changing every class in the chain. That is where **kwargs comes in.

---

### Exercise 3. **kwargs

**kwargs lets a function accept any number of keyword arguments. Instead of explicitly listing every optional parameter at each level, we use **kwargs to collect them and pass them up the chain via super():

lab_week_5.py (final version with **kwargs):

```python
class Vehicle:
    def __init__(self, colour, weight, max_speed, max_range=None, seats=None):
        self.colour = colour
        self.weight = weight
        self.max_speed = max_speed
        self.max_range = max_range
        self.seats = seats

    def move(self, speed):
        print(f"The vehicle is moving at {speed} km/h")

class Car(Vehicle):
    def __init__(self, colour, weight, max_speed, form_factor, **kwargs):
        super().__init__(colour, weight, max_speed, **kwargs)
        self.form_factor = form_factor

    def move(self, speed):
        print(f"The car is driving at {speed} km/h")

class Electric(Car):
    def __init__(self, colour, weight, max_speed, form_factor, battery_capacity, **kwargs):
        super().__init__(colour, weight, max_speed, form_factor, **kwargs)
        self.battery_capacity = battery_capacity

    def move(self, speed):
        print(f"The electric car is driving at {speed} km/h and has a maximum range of {self.max_range} km")

class Petrol(Car):
    def __init__(self, colour, weight, max_speed, form_factor, fuel_capacity, **kwargs):
        super().__init__(colour, weight, max_speed, form_factor, **kwargs)
        self.fuel_capacity = fuel_capacity

    def move(self, speed):
        print(f"The petrol car is driving at {speed} km/h")
```

Now we can add new optional attributes to Vehicle (like seats) without changing any of the child classes. They just pass **kwargs through:

```python
generic_electric_car = Electric("red", 1000, 200, "SUV", 100, max_range=500, seats=5)
generic_electric_car.move(100)
print(generic_electric_car.seats)  # 5
```

The task is to also add the Plane hierarchy (with Propeller and Jet subclasses) using the same **kwargs pattern. Plane gets a wingspan attribute, Propeller gets propeller_diameter, Jet gets engine_thrust.

---

## Section 3: Multiple Inheritance

A FlyingCar is both a Car and a Plane. Python supports this through multiple inheritance, listing both parent classes separated by a comma:

lab_week_5.py (with FlyingCar):

```python
class FlyingCar(Car, Plane):
    def __init__(self, colour, weight, max_speed, form_factor, wingspan, **kwargs):
        super().__init__(colour, weight, max_speed, form_factor=form_factor, wingspan=wingspan, **kwargs)

    def move(self, speed):
        print(f"The flying car is driving or flying at {speed} km/h")

generic_flying_car = FlyingCar("red", 1000, 200, "SUV", 30, seats=5)
generic_flying_car.move(100)
print(generic_flying_car.seats, generic_flying_car.wingspan, generic_flying_car.form_factor)
```

The super().__init__() call passes form_factor and wingspan as keyword arguments so that following Python's MRO (Method Resolution Order), both Car and Plane get the arguments they need. We can access attributes from both parents on the resulting object.

When there are many arguments, using keyword arguments for all of them makes the code clearer:

```python
generic_flying_car_2 = FlyingCar(colour="red", weight=1000, max_speed=200, form_factor="SUV", wingspan=30, seats=5)
```

The lab also briefly mentions mixins, which are a way to add functionality to a class without inheriting from it. They are not commonly used but worth understanding conceptually.

---

## Section 4: Polymorphism

Polymorphism means the same method name behaves differently depending on the object's type. All our vehicle classes have a move method, but each prints a different message. The key term is method overriding: the child class redefines a method from the parent.

This is powerful because we can write code that works with any "movable" object without knowing its exact type:

lab_week_5.py (polymorphism demo):

```python
class Animal:
    def move(self, speed):
        print(f"The animal is moving at a speed of {speed}")

generic_animal = Animal()

for movable_object in [generic_vehicle, generic_electric_car, generic_flying_car, generic_animal]:
    movable_object.move(20)
```

Even though Animal has no relation to Vehicle, it also has a move method. The loop calls move(20) on each object and the correct version runs every time. This is polymorphism in action.

Note: Python does not support method overloading (having multiple methods with the same name but different parameters in the same class). Other languages like Java do.

---

## Section 6: ToDo App, RecurringTask

Now we apply inheritance to the ToDoApp. Tasks are often not one-time things: you might do laundry every week or clean your room every two weeks. We create a RecurringTask class that inherits from Task.

tasks.py:

```python
import datetime

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
```

RecurringTask inherits everything from Task via super().__init__(title, date_due) and adds:
- interval: a timedelta object indicating how often the task repeats (e.g. every 7 days)
- completed_dates: a list of datetime objects tracking when the task was completed each time
- _compute_next_due_date: a private method (prefixed with _) that calculates the next due date by adding the interval to the current due date
- mark_completed is overridden (polymorphism): instead of just setting completed to True, it appends the current time to completed_dates and advances the due date to the next occurrence
- __str__ is also overridden to show the recurring-specific information

The main.py is updated to handle recurring tasks. When the user adds a task, they are asked if it is recurring. If yes, they enter an interval in days:

main.py:

```python
from tasklist import TaskList
from tasks import Task, RecurringTask
import datetime

def propagate_task_list(task_list: TaskList) -> TaskList:
    task_list.add_task(Task("Buy groceries", datetime.datetime.now() - datetime.timedelta(days=4)))
    task_list.add_task(Task("Do laundry", datetime.datetime.now() - datetime.timedelta(days=-2)))
    task_list.add_task(Task("Clean room", datetime.datetime.now() + datetime.timedelta(days=-1)))
    task_list.add_task(Task("Do homework", datetime.datetime.now() + datetime.timedelta(days=3)))
    task_list.add_task(Task("Walk dog", datetime.datetime.now() + datetime.timedelta(days=5)))
    task_list.add_task(Task("Do dishes", datetime.datetime.now() + datetime.timedelta(days=6)))

    r_task = RecurringTask("Go to the gym", datetime.datetime.now(), datetime.timedelta(days=7))
    r_task.completed_dates.append(datetime.datetime.now() - datetime.timedelta(days=7))
    r_task.completed_dates.append(datetime.datetime.now() - datetime.timedelta(days=14))
    r_task.completed_dates.append(datetime.datetime.now() - datetime.timedelta(days=22))
    r_task.date_created = datetime.datetime.now() - datetime.timedelta(days=28)
    task_list.add_task(r_task)

    return task_list

def main() -> None:
    task_list = TaskList("YOUR NAME")
    task_list = propagate_task_list(task_list)

    while True:
        print("To-Do List Manager")
        print("1. Add a task")
        print("2. View tasks")
        print("3. Remove a task")
        print("4. Edit a task")
        print("5. Complete a task")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter a task: ")
            input_date = input("Enter a due date (YYYY-MM-DD): ")
            date_object = datetime.datetime.strptime(input_date, "%Y-%m-%d")
            recurring = input("Is this a recurring task? (y/n): ")
            if recurring == "y":
                interval = int(input("Enter the interval between each repetition (days): "))
                recurring_task = RecurringTask(title, date_object, interval=datetime.timedelta(days=interval))
                task_list.add_task(recurring_task)
            else:
                task = Task(title, date_object)
                task_list.add_task(task)

        elif choice == "2":
            task_list.view_tasks()

        elif choice == "3":
            ix = int(input("Enter the index of the task to remove: "))
            task_list.remove_task(ix)

        elif choice == "4":
            ix = int(input("Enter the index of the task to edit: "))
            choice = input("What would you like to edit? (title/due date): ")
            if choice == "title":
                title = input("Enter a new title: ")
                task_list.get_task(ix).change_title(title)
            elif choice == "due date":
                input_date = input("Enter a new due date (YYYY-MM-DD): ")
                date_object = datetime.datetime.strptime(input_date, "%Y-%m-%d")
                task_list.get_task(ix).change_date_due(date_object)
            else:
                print("Invalid choice.")

        elif choice == "5":
            ix = int(input("Enter the index of the task to complete: "))
            task_list.get_task(ix).mark_completed()

        elif choice == "6":
            break

if __name__ == "__main__":
    main()
```

When choice 5 is used on a recurring task, mark_completed() on RecurringTask runs (not the one from Task) thanks to polymorphism. This adds the current date to completed_dates and advances the due date.

---

## Exercise 4: Encapsulation

In the main function, choices 4 and 5 access tasks directly via task_list.tasks[ix]. This bypasses the TaskList class and directly accesses its internal data. Encapsulation says we should hide the inner workings and provide controlled access through methods instead.

The fix is to add a get_task method to TaskList:

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
        for ix, task in enumerate(self.tasks):
            print(f"{ix}: {task}")
```

Now main.py uses task_list.get_task(ix) instead of task_list.tasks[ix]. The benefit is that if we later change how tasks are stored internally (say, in a database instead of a list), we only need to update get_task. The main function does not need to know or care about the storage details.

---

## Section 7: Portfolio Exercises

Portfolio Exercise 3 asks us to expand the ToDoApp with user and owner classes:
- Create a User class with name and email attributes
- Create an Owner class that inherits from User
- Modify TaskList so its owner attribute is of type Owner instead of a plain string
- Update the UML diagram to reflect these changes

Portfolio Exercise 4 asks us to implement the above in code:
- Create a users.py module containing both User and Owner classes with __str__ methods
- Modify TaskList to accept an Owner object in its __init__
- Update main.py to create an Owner instance and pass it when constructing the TaskList

---

## Python Files

### lab_week_6_debugging.py

A Car class with a simple interactive program for debugging practice:

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

There is a bug in this code: the __init__ method has speed:str=0 as the type hint, suggesting a string, but the default value is 0 (an integer). The type hint is wrong but the code still runs because Python does not enforce type hints at runtime. The accelerate and brake methods use += and -= which work fine on integers. If someone actually passed a string like Car("fast"), the arithmetic would fail.
