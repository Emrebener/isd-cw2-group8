# Week 5: Testing and GUI

Module: COMP11124 Interactive Software Design
Materials: Week 5.pdf, lab_week_5.py

Topics covered: Testing programs with pytest, running programs in a GUI window with tkinter

Note: The exercises this week are bonus material and not part of the module assessment. They are provided for students who are up to date with Sessions 1-4.

---

## Section 1: Testing

### Exercise 1. Factorial

This exercise introduces pytest, a Python package for writing and running tests. The idea is that instead of manually running a program and checking the output, you write test functions that automatically verify your code produces the correct results.

First we install pytest with pip install -U pytest and confirm with pytest --version.

The project structure separates source code and tests into different folders:

```
session_bonus/
    factorial/
        src/
            factorial.py
        tests/
            test_factorial.py
```

The factorial function calculates n! recursively. The initial version:

```python
def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)
```

To test it, we create test_factorial.py:

```python
import pytest
from src.factorial import factorial

def test_factorial_basic():
    assert factorial(5) == 120
```

Running pytest from the root folder (factorial/) picks up any files prefixed with test_. The first run passes: factorial(5) correctly returns 120.

But the initial version has edge case problems. We expand the tests to cover more cases:

```python
import pytest
from src.factorial import factorial

def test_factorial_basic():
    assert factorial(5) == 120
    assert factorial(3) == 6

def test_factorial_zero_and_one():
    assert factorial(0) == 1
    assert factorial(1) == 1

def test_factorial_negative_error():
    with pytest.raises(ValueError):
        factorial(-1)
```

Running these tests now fails spectacularly: factorial(0) causes infinite recursion (since 0 never equals 1), and factorial(-1) does the same instead of raising an error.

The fix is to update factorial.py to handle these edge cases:

```python
def factorial(n):
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
```

Now all 3 tests pass. Each test gets a fresh instance of the function being tested, so one failure does not prevent later tests from running.

Note: running pytest leaves a .pytest_cache folder in the project root. An alternative to using the pytest command directly is python -m pytest, which requires adding an __init__.py file to the src folder and a conftest.py to the root folder:

```python
# conftest.py
import sys
from pathlib import Path

src_path = Path(__file__) / "src"
sys.path.insert(0, str(src_path))
```

This adds the src directory to the Python path so the test files can import from it.

---

### Exercise 2. Temperature

This exercise applies the same testing approach to the temperature converter from earlier weeks. The project structure follows the same pattern:

```
session_bonus/
    temperature/
        src/
            __init__.py
            temperature_converter_function.py
        tests/
            test_temperature_converter_function.py
        conftest.py
```

The temperature converter is refactored from a standalone script into a function that can be imported and tested. The convert function takes a temperature scale (C, F, or K) and a temperature value as strings, then returns all three conversions:

```python
scales = ["C", "F", "K"]

def convert(temperature_scale:str = "C", temperature_input:str = "0"):
    if scales.index(temperature_scale) == 0:  # Celsius
        degree_celcius = float(temperature_input)
        degree_fahrenheit = (degree_celcius * 9/5) + 32
        degree_kelvin = degree_celcius + 273.15
    elif scales.index(temperature_scale) == 1:  # Fahrenheit
        degree_fahrenheit = float(temperature_input)
        degree_celcius = (degree_fahrenheit - 32) * 5/9
        degree_kelvin = (degree_fahrenheit + 459.67) * 5/9
    elif scales.index(temperature_scale) == 2:  # Kelvin
        degree_kelvin = float(temperature_input)
        degree_celcius = degree_kelvin - 273.15
        degree_fahrenheit = (degree_kelvin - 273.15) * 9/5 + 32
    return degree_celcius, degree_fahrenheit, degree_kelvin

if __name__ == "__main__":
    temperature_scale = ("Enter the temperature scale you want to convert from: \n 'C' Celcius \n 'F' Fahrenheit \n 'K'. Kelvin \n")
    temperature_scale = input(temperature_scale).strip().upper()
    if temperature_scale not in scales:
        print("Invalid scale. Please enter 'C', 'F', or 'K'.")
        exit()
    temperature_input = input(f"Enter the temperature in {temperature_scale}: ")

    degree_celcius, degree_fahrenheit, degree_kelvin = convert(temperature_scale, temperature_input)

    print("Temperature Conversion Results:")
    print(f"{degree_celcius} degree Celsius")
    print(f"{degree_fahrenheit} degree Farenheit")
    print(f"{degree_kelvin} degree Kelvin")
    print("Thank you for using the Temperature Converter!")
```

The if __name__ == "__main__" guard means the user input/print code only runs when the script is executed directly. When imported by a test file, only the convert function is available.

A basic test:

```python
import pytest
from src.temperature_converter_function import convert

def test_temperature_converter():
    celsius, fahrenheit, kelvin = convert("C", "0")
    assert celsius == pytest.approx(0, abs=0.01)
    assert fahrenheit == pytest.approx(32.0, abs=0.01)
    assert kelvin == pytest.approx(273.15, abs=0.01)
```

pytest.approx is used because floating point arithmetic can produce tiny rounding differences. The abs=0.01 parameter allows results within 0.01 of the expected value.

To test multiple inputs without writing separate test functions, pytest.mark.parametrize feeds a list of test cases into a single function:

```python
import pytest
from src.temperature_converter_function import convert

@pytest.mark.parametrize(
    "scale, temp, expected_celsius, expected_fahrenheit, expected_kelvin",
    [
        ("C", "0", 0.0, 32.0, 273.15),
        ("F", "32", 0.0, 32.0, 273.15),
        ("K", "273.15", 0.0, 32.0, 273.15),
        ("Z", "273.15", 0.0, 32.0, 273.15),
    ],
)
def test_temperature_converter(scale, temp, expected_celsius, expected_fahrenheit, expected_kelvin):
    celsius, fahrenheit, kelvin = convert(scale, temp)
    assert celsius == pytest.approx(expected_celsius, abs=0.01)
    assert fahrenheit == pytest.approx(expected_fahrenheit, abs=0.01)
    assert kelvin == pytest.approx(expected_kelvin, abs=0.01)
```

The first three test cases (C, F, K) all pass because 0 Celsius, 32 Fahrenheit, and 273.15 Kelvin are the same temperature. The fourth case ("Z") fails with a ValueError because "Z" is not in the scales list. This reveals a bug: the program crashes on invalid input instead of handling it gracefully.

Tasks:
- Modify temperature_converter_function.py so that an invalid temperature scale does not cause a crash
- Add minimum physical value checks for each scale (0 K, -273.15 C, -459.67 F) and reject temperatures below those

---

### Exercise 3. To-Do List

This exercise applies testing to the to-do list program from earlier sessions. The structure:

```
session_bonus/
    to_do_list/
        src/
            to_do_list.py
        tests/
            test_to_do_list.py
        conftest.py
```

The to-do list code:

```python
tasks = []

def add_task(list):
    list.append(input("Add a task: "))

def view_tasks(list):
    count = 0
    for element in list:
        print(f"{count + 1}.{element}")
        count += 1
    print("Total tasks:", len(list), "\n")

def remove_task(list):
    choice = input("Task number to remove: ")
    choice = int(choice)-1
    if not (choice in range(len(list))):
        print("Invalid task number.")
        return
    list.remove(list[choice])

def main():
    while True:
        print("\n")
        print("To-Do List Manager")
        print("1. Add a task")
        print("2. View tasks")
        print("3. Remove a task")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            remove_task(tasks)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again. \n")

if __name__ == "__main__":
    main()
```

Testing this program is trickier because the functions use input() for user interaction. You can't just call them normally from a test. The solution is monkeypatch, a pytest feature that lets you temporarily replace built-in functions. We replace input() with a lambda that iterates through a predefined list of responses:

```python
from src.to_do_list import main, tasks

def test_main_choice_1_add_task(monkeypatch):
    """Test choice 1: Add a task"""
    tasks.clear()
    inputs = iter(["1", "Buy groceries", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main()
    assert "Buy groceries" in tasks

def test_main_choice_2_view_tasks(monkeypatch, capsys):
    """Test choice 2: View tasks"""
    tasks.clear()
    tasks.append("Task 1")
    tasks.append("Task 2")
    inputs = iter(["2", "4"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main()
    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Task 2" in captured.out
    assert "Total tasks: 2" in captured.out

def test_main_choice_3_remove_tasks(monkeypatch, capsys):
    """Test choice 3: Remove tasks"""
    tasks.clear()
    tasks.append("Task 1")
    tasks.append("Task 2")
    inputs = iter(["3", "2", "4"])  # remove task 2, view, quit
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    main()
    assert "Task 2" not in tasks
```

monkeypatch.setattr('builtins.input', lambda _: next(inputs)) replaces the built-in input() function with a lambda that pops the next value from our predefined list each time input() is called. The capsys fixture captures stdout so we can assert against what was printed.

Tasks:
- Add an error into to_do_list.py and confirm the tests catch it
- Add a test that checks an invalid menu choice does not crash the program
- Refactor the test file so menu choices are stored as variables at the top

---

## Section 2: GUI Programming

### Exercise 1. Tkinter To-Do List

tkinter is a Python library for building windowed GUI interfaces. It comes built into Python as a wrapper around Tcl/Tk.

The exercise provides a full tkinter implementation of the to-do list. The window is built with a grid layout of two rows and two columns:

- Left frame (row 0, column 0): holds a "Menu" label and three buttons: Add Task, Remove Task, Quit
- Right frame (row 0, column 1): holds a "Tasks" label and a Listbox that displays tasks
- Input frame (row 1, spanning both columns): holds a label and an Entry widget for text input

The main entry point:

```python
import tkinter as tk
from tkinter import messagebox

tasks = []
root = None
tasks_listbox = None
input_entry = None
input_label = None
current_input_callback = None

def main():
    create_main_window()

if __name__ == "__main__":
    main()
```

create_main_window() sets up the root Tk window at 600x400 pixels, creates the three frames, configures the grid layout, and starts the mainloop which keeps the window running and responsive.

The flow for adding a task: pressing "Add Task" calls add_task_gui(), which sets current_input_callback to process_task and displays a prompt in the input frame. When the user types something and presses Enter, handle_input_entry() is triggered, which calls the current callback (process_task) with the entered text. process_task appends the task to the list and calls update_tasks_display() to refresh the Listbox.

Removing a task works similarly: remove_task_gui() checks if there are tasks, then prompts for a task number. It validates the input (must be a valid integer within range), removes the task, and updates the display. Invalid inputs show error dialogs via messagebox.showerror().

The Quit button simply calls parent.quit which closes the window.

---

## Python File

### lab_week_5.py

This file contains the Vehicle inheritance hierarchy used as a code example for the week. It is not directly related to the lab exercises above but demonstrates inheritance and polymorphism:

```python
class Vehicle:
    def __init__(self, color, weight, max_speed, max_range=None, seats=None):
        self.color = color
        self.weight = weight
        self.max_speed = max_speed
        self.max_range = max_range
        self.seats = seats

    def move(self, speed):
        print(f"The vehicle is moving at {speed} km/h")

class Car(Vehicle):
    def __init__(self, color, weight, max_speed, form_factor, **kwargs):
        super().__init__(color, weight, max_speed, **kwargs)
        self.form_factor = form_factor

    def move(self, speed):
        print(f"The car is driving at {speed} km/h")

class Plane(Vehicle):
    def __init__(self, color, weight, max_speed, wingspan, **kwargs):
        super().__init__(color, weight, max_speed, **kwargs)
        self.wingspan = wingspan

    def move(self, speed):
        print(f"The plane is flying at {speed} km/h")

class Electric(Car):
    def __init__(self, color, weight, max_speed, form_factor, battery_capacity, **kwargs):
        super().__init__(color, weight, max_speed, form_factor, **kwargs)
        self.battery_capacity = battery_capacity

    def move(self, speed):
        print(f"The electric car is driving at {speed} km/h and has a maximum range of {self.max_range} km")

class Petrol(Car):
    def __init__(self, color, weight, max_speed, form_factor, fuel_capacity, **kwargs):
        super().__init__(color, weight, max_speed, form_factor, **kwargs)
        self.fuel_capacity = fuel_capacity

    def move(self, speed):
        print(f"The petrol car is driving at {speed} km/h")

class Propeller(Plane):
    def __init__(self, color, weight, max_speed, wingspan, propeller_diameter, **kwargs):
        super().__init__(color, weight, max_speed, wingspan, **kwargs)
        self.propeller_diameter = propeller_diameter

    def move(self, speed):
        print(f"The propeller plane is flying at {speed} km/h")

class Jet(Plane):
    def __init__(self, color, weight, max_speed, wingspan, engine_thrust, **kwargs):
        super().__init__(color, weight, max_speed, wingspan, **kwargs)
        self.engine_thrust = engine_thrust

    def move(self, speed):
        print(f"The jet plane is flying at {speed} km/h")

class FlyingCar(Car, Plane):
    def __init__(self, color, weight, max_speed, form_factor, wingspan, **kwargs):
        super().__init__(color, weight, max_speed, form_factor=form_factor, wingspan=wingspan, **kwargs)

    def move(self, speed):
        print(f"The flying car is driving at {speed} km/h")
```

The hierarchy is: Vehicle at the top, with Car and Plane inheriting from it. Electric and Petrol inherit from Car. Propeller and Jet inherit from Plane. FlyingCar inherits from both Car and Plane (multiple inheritance).

Each subclass calls super().__init__() to pass arguments up to the parent class. The **kwargs pattern allows optional arguments like max_range and seats to flow through the chain without every class needing to list them explicitly.

Every class overrides the move() method with its own message. This is polymorphism: the same method name behaves differently depending on the actual type of the object. The file demonstrates this at the end:

```python
for movable_object in [generic_vehicle, generic_electric_car, generic_flying_car, generic_animal]:
    movable_object.move(20)
```

Even though we call .move(20) on each object, the output differs because each class has its own implementation. An Animal class (unrelated to Vehicle) also has a move method, showing that polymorphism works based on the method name, not the class hierarchy.
