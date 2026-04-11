# Week 2 -- Introduction to Python Programming II

**Module:** COMP11124 Object Oriented Programming
**Materials:** `Week2.pdf`, `code.py`, `code-solutions.py`

**Topics covered:** Comparisons and Conditionals, Lists, Loops, Input

---

## Exercise 1.1. Comparison Operators

This exercise introduces comparisons in Python. A comparison always returns a Boolean value -- either `True` or `False`.

You can store a Boolean directly like `is_true = True` (no quotes -- it's not a string). But more usefully, you can store the result of a comparison:

```python
is_true = 5 > 4  # True
```

The comparison operators are:
- `<` (less than), `>` (greater than)
- `==` (equal), `!=` (not equal)
- `<=` (less than or equal to), `>=` (greater than or equal to)

The task is to try each of these on W3Schools and change the values to make them return `False`.

---

## Exercise 1.2. Logical Operators

Sometimes a single comparison isn't enough. For example, checking if someone's age is between 20 and 30 requires two comparisons combined. That's what logical operators are for.

Python has three:
- **`and`** -- returns `True` only if both sides are `True`
- **`or`** -- returns `True` if at least one side is `True`
- **`not`** -- flips `True` to `False` and vice versa

Example:

```python
age = 25
is_in_age_range = age > 20 and age < 30  # True
```

---

## Exercise 1.3. `if` Conditionals

This is where we start controlling program flow based on comparisons. A basic `if` statement checks a condition and runs the indented code block only if it's `True`.

```python
age = 19
age_group = "child"

if age > 18:
    age_group = "adult"

print(f"The age group is {age_group}")
```

We set a default `age_group` of `"child"`, then the `if` statement overwrites it to `"adult"` only when the condition holds. The indented block (4 spaces or 1 tab) is what belongs to the `if`. The task is to run this with different ages and see how the output changes.

---

## Exercise 1.4. `if-else` Conditionals

A plain `if` only handles one case. `if-else` gives us two branches -- one for when the condition is `True`, one for when it's `False`. Only one of them runs.

```python
wind_speed = 30

if wind_speed < 10:
    print("It is a calm day")
else:
    print("It is a windy day")
```

Since `wind_speed` is 30 (not less than 10), the `else` branch executes and we get "It is a windy day".

---

## Exercise 1.5. `if-elif-else` Conditionals

When there are more than two possible outcomes, we chain `elif` (else-if) blocks between `if` and `else`. The example is a grading system:

```python
grade = 55

if grade < 50:
    print("You failed")
elif grade < 60:
    print("You passed")
elif grade < 70:
    print("You got a good pass")
else:
    print("You got an excellent pass")
```

Python checks each condition top to bottom and executes the first one that's `True`. Once a match is found, the rest are skipped entirely. So with `grade = 55`, the first check (`< 50`) fails, the second (`< 60`) succeeds, and it prints "You passed" -- the remaining `elif`/`else` blocks don't even get evaluated.

---

## Exercise 1.6. Summary Tasks

**Task -- Compare Temperatures:** Create two variables `temperature1` and `temperature2` with different values. Use an `if` statement to check if they're equal and print a message, and an `else` to print a different message if they're not.

---

## Exercise 2.1. Creating a List

Lists are mutable collections defined with square brackets. They're indexed starting from 0 and can hold mixed data types.

```python
integer_list = [1, 2, 3, 4, 5]
string_list = ["apple", "banana", "orange", "grape"]
empty_list = []
list_with_different_types = [1, "two", 3.0, True]
```

You can also build lists from existing variables:

```python
person_1_age = 20
person_2_age = 30
age_list = [person_1_age, person_2_age]
```

Lists can even be nested: `[["red", "green", "blue"], ["yellow", "orange", "purple"]]`.

The task is to create a `city_list` containing `"Glasgow"`, `"London"`, `"Edinburgh"`.

---

## Exercise 2.2. Accessing a List

Individual items are accessed by index: `string_list[0]` returns `"apple"`. Negative indices count from the end: `string_list[-1]` returns `"grape"`.

**Slicing** lets you grab a range: `string_list[0:2]` returns `["apple", "banana"]` -- the end index is exclusive.

The task is to print the third item in `city_list` and use slicing to get the last two items.

---

## Exercise 2.3. Modifying a List

You can change items by index (`string_list[0] = "pear"`) or add to the end with `append()`:

```python
string_list.append("orange")
```

The task is to append `"Manchester"` to `city_list` and change the second item to `"Birmingham"`.

---

## Exercise 2.4. Summary Task -- Create, Access and Modify Lists

A combined task that tests everything covered about lists:
- Create a `colours` list with 3 colour strings
- Print it, access the second element, modify the first element
- Check the length with `len()`
- Use a conditional to check if `"red"` is in the list (using `in`)
- Use slicing to create a `selected_colours` list from the 2nd and 3rd elements

---

## Exercise 3.1. While Loops

A `while` loop keeps running as long as its condition is `True`.

```python
i = 0
while i < 5:
    print(i)
    i += 1
```

This prints 0 through 4. The `+=` operator is shorthand for `i = i + 1`. Important: if the condition never becomes `False`, you get an infinite loop -- use Ctrl+C to kill it.

---

## Exercise 3.2. For Loops

A `for` loop iterates over a sequence (like a list):

```python
for fruit in string_list:
    print(fruit)
```

The variable `fruit` takes the value of each item in the list, one at a time. The name is arbitrary but should be descriptive.

The task is to create a `for` loop that prints each item in `city_list`.

---

## Exercise 3.3. Loop Keywords: `range`, `break` and `continue`

**`range()`** generates a sequence of numbers. Some forms:
- `range(5)` -> 0, 1, 2, 3, 4
- `range(0, 5, 2)` -> 0, 2, 4 (third parameter is the step)
- `range(5, 0, -1)` -> 5, 4, 3, 2, 1

**`break`** exits the loop early:

```python
for i in range(5):
    if i == 2:
        break
    print(i)
# prints 0, 1
```

**`continue`** skips the rest of the current iteration and moves to the next one:

```python
for i in range(5):
    if i == 2:
        continue
    print(i)
# prints 0, 1, 3, 4
```

---

## Exercise 3.4. Summary Tasks

**Task -- Even Numbers:** Create a list of integers 1 to 10, loop through it, and only print the even ones (using `% 2 == 0`).

**Task -- Sum of Squares:** Initialize `sum_of_squares = 0`, loop through 1 to 5 with `range()`, add the square of each number. Result should be 55 (1 + 4 + 9 + 16 + 25).

**Task -- Countdown:** Set `countdown = 10`, use a `while` loop to count down to 1, then print `"Liftoff!"`.

---

## Exercise 4.1. Obtaining User Input

The `input()` function pauses the program and waits for the user to type something. It always returns a string, so you need to cast it if you want a number.

```python
user_input = input("Enter something: ")
print("You entered:", user_input)
```

For numbers:

```python
age = input("How old are you? ")
age = int(age)
next_year_age = age + 1
print("Next year, you'll be", next_year_age, "years old.")
```

**Task -- User Input and Conditional Statements:** Take the user's age as input. If under 18, print "You are a minor." If between 18 and 65 (inclusive), print "You are an adult." If over 65, print "You are a senior citizen."

**Task -- Temperature Converter:** Modify last week's temperature converter to take user input via `input()` instead of hardcoding a value. As an extra task, let the user choose which unit (C, K, or F) they want to convert from, and use conditionals to handle each case.

---

## Python Files

### `code.py`

This is a To-Do List Manager -- an interactive program that ties together lists, loops, functions, conditionals, and user input. It uses a `while True` loop as the main program loop with a menu system:

```python
tasks = []

def add_task(task):
    tasks.append(task)

def view_tasks():
    for ix, task in enumerate(tasks):
        print(ix, task)

def remove_task(ix):
    del tasks[ix]

while True:
    print("--------------------")
    print("To-Do List Manager")
    print("1. Add a task")
    print("2. View tasks")
    print("3. Remove a task")
    print("4. Quit")

    choice = input("Enter your choice: ")

    if choice == "1":
        task = input("Enter a task: ")
        add_task(task)
    elif choice == "2":
        print("--------------------")
        print("Current tasks:")
        view_tasks()
    elif choice == "3":
        view_tasks()
        ix = int(input("Enter the index of the task to remove: "))
        remove_task(ix)
    elif choice == "4":
        break
    else:
        print("Invalid choice. Please try again.")
```

A few things to note:
- `enumerate(tasks)` gives both the index and the value for each item, which is used for display and removal
- `del tasks[ix]` removes a list item by index
- The `while True` loop runs forever until the user picks option 4, which triggers `break`
- `input()` always returns a string, so `choice` is compared against string `"1"`, `"2"`, etc. -- and `int()` is used when we need a numeric index for removal

### `code-solutions.py`

This file contains solutions to three function-based exercises:

**1. Greeting friends** -- iterates over a list and prints a greeting for each:

```python
friend_list = ["John", "Jane", "Jack"]

def greet_friends(friends):
    for friend in friends:
        print(f"Hello {friend}!")

greet_friends(friend_list)
```

**2. Tax calculator** -- a simple function with two parameters that returns a value:

```python
def calculate_tax(income, tax_rate):
    return income * tax_rate

print(calculate_tax(50000, 0.2))  # 10000.0
```

**3. Compound interest calculator** -- includes input validation and a loop:

```python
def compound_interest(principal, interest_rate, duration):
    if interest_rate < 0 or interest_rate > 1:
        print("Please enter a decimal number between 0 and 1")
        return None
    if duration < 0:
        print("Please enter a positive number of years")
        return None
    for i in range(1, duration + 1):
        investment_value = principal * (1 + interest_rate) ** i
        print(f"The total amount of money earned by the investment is {int(investment_value)} £")
    return int(investment_value)

print(compound_interest(1000, 0.03, 5))
```

This one validates inputs with conditionals (returning `None` early if invalid), then uses a `for` loop with `range()` to calculate the compound interest year by year. The formula `principal * (1 + interest_rate) ** i` uses the exponentiation operator from Week 1.
