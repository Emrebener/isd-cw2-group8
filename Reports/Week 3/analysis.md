# Week 3 -- Python Functions, Scope and Errors

Module: COMP11124 Object Oriented Programming
Materials: Week 3.pdf, code.py, code-solutions.py

Topics covered: Functions, Scope, Assertions, Common Python Errors

---

## Exercise 1.1. Functions in Python

This exercise introduces functions. A function is a reusable block of code that only runs when it's called. You define one with the def keyword, followed by the function name and parentheses ending with a colon.

A basic function with no parameters:

```python
def greet_user():
    print("Hello!")

greet_user()
```

Functions can also take parameters -- variables listed inside the parentheses that only exist within the function. For example:

```python
def greet_user(name):
    print(f"Hello {name}!")

greet_user("John")
```

Here, name is the parameter (defined in the function) and "John" is the argument (the value passed when calling it).

You can have multiple parameters by separating them with commas:

```python
def greet_user(first_name, last_name):
    print(f"Hello {first_name} {last_name}!")

greet_user("John", "Smith")
```

When calling the function, the order matters and you need to pass the correct number of arguments.

Keyword arguments let you pass arguments in any order by specifying the parameter name:

```python
greet_user(last_name="Smith", first_name="John")
```

Default values can be set for parameters so they're optional when calling. For example, setting a default university:

```python
def greet_user(first_name, last_name, university="UWS"):
    print(f"Hello {first_name} {last_name} from {university}!")
```

Calling greet_user("John", "Smith") would output "Hello John Smith from UWS!" but you can override it by passing a third argument like greet_user("John", "Smith", "UWS London").

The task is to create a greet_friends function that takes a list of names and prints "Hello" followed by each name using a for loop.

---

## Exercise 1.2. Return Values

Functions can also return values using the return keyword. This lets us use the result elsewhere in our code instead of just printing inside the function.

```python
def add_numbers(num1, num2):
    return num1 + num2

result = add_numbers(5, 10)
print(result)
```

You can also return multiple values separated by commas:

```python
def add_and_multiply_numbers(num1, num2):
    return num1 + num2, num1 * num2

sum, product = add_and_multiply_numbers(5, 10)
```

An important thing the lab points out: the variable name result used inside the function and the one used outside are two different variables. They just happen to share the same name. This ties into variable scope, which is covered in the next exercise.

---

## Exercise 1.3. Task -- Tax Calculation

We define a calculate_tax function that takes income and tax_rate as parameters, multiplies them, and returns the result:

```python
def calculate_tax(income, tax_rate):
    return income * tax_rate

print(calculate_tax(50000, 0.2))
```

This prints 10000.0.

---

## Exercise 1.4. Task -- Compound Interest Calculator

This is a more involved function. It takes principal, interest_rate, and duration as parameters, validates the inputs, and calculates compound interest year by year.

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

The function first checks if the inputs are valid -- if the interest rate is outside 0 to 1 or the duration is negative, it prints an error message and returns None early. Otherwise, it loops through each year using range(1, duration + 1) and calculates the total using the formula: principal * (1 + interest_rate) ** year. It converts the final result to an integer with int() before returning. Calling compound_interest(1000, 5, 0.03) should return 1159 for year 5.

---

## Exercise 2. Variable Scope

Variable scope refers to where in the code a variable can be accessed. A variable defined inside a function has local scope -- it only exists within that function.

```python
def new_function():
    my_new_variable = 5

new_function()
print(my_new_variable)  # this will cause an error
```

The print line will fail because my_new_variable was defined inside new_function and doesn't exist outside it.

An important gotcha: if you have a variable with the same name both inside and outside a function, they are two separate variables.

```python
my_new_variable = 0

def new_function():
    my_new_variable = 5

new_function()
print(my_new_variable)  # prints 0, not 5
```

The function creates its own local my_new_variable which shadows the global one but doesn't change it. The global variable remains 0.

Local scope only applies to functions. Variables defined inside if statements or loops are still in global scope and can be accessed outside of them.

---

## Exercise 6. Assertions

Assertions are used to validate that certain conditions hold during execution. If the condition is False, Python raises an AssertionError.

For example, to verify the compound interest function works correctly:

```python
assert compound_interest(1000, 5, 0.03) == 1159
```

If the function returns 1159, the assertion passes silently. If it returns anything else, the program crashes with an error. Assertions are useful for debugging and making sure your code produces expected results.

---

## Exercise 7. Identifying and Fixing Common Errors

This exercise covers two categories of errors:

Logical errors happen when the code runs fine but produces wrong results. For example, using - instead of + in an addition function. The program won't crash, it just gives the wrong answer.

Semantic errors cause the program to crash or produce error messages. The common types covered:

Syntax Error -- code violates Python's syntax rules. Example: print("Hello World!) is missing the closing quote.

Name Error -- a variable or name is not defined or misspelled. Example: defining my_name = "Alice" but then trying to print myname (missing the underscore).

Value Error -- a function receives the right type but an inappropriate value. Example: int("Hello World") tries to convert a non-numeric string to an integer.

Index Error -- accessing an index that doesn't exist. Example: fruits = ["apple", "banana", "orange"] then fruits[3] tries to access a 4th element that isn't there (indices go 0, 1, 2).

Indentation Error -- code is not indented correctly. Example: the print statement after an if block is not indented, so Python doesn't know it belongs to the if.

The error-fixing tasks:
- Syntax error: pritn("Hello, World!") should be print("Hello, World!")
- Name error: favorite_color is not defined before being used in the print statement -- need to add favorite_color = "Blue" before the print
- Value error: number1 = "5" is a string, so number1 + number2 concatenates instead of adding -- change it to number1 = 5 (without quotes)
- Index error: fruits[3] on a 3-item list should be fruits[1] to get the second element
- Indentation error: the print("Good morning!") line needs to be indented under the if block

---

## Exercise 3.1. To-Do List Manager

This is the final exercise that combines everything from the past 3 weeks: variables, lists, loops, functions, conditionals, and user input.

We build a to-do list manager with a menu-driven while True loop. The program has three functions: add_task to append a task to the list, view_tasks to display all tasks with their indices using enumerate, and remove_task to delete a task by index using del.

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

The menu runs in a while True loop that only exits when the user picks option 4 (which triggers break). Each option calls the appropriate function. enumerate(tasks) in view_tasks gives both the index and the task, which is needed for the remove feature. The choice variable is compared as a string since input() always returns a string.

---

## Python Files

### code.py

This is the completed to-do list manager described in Exercise 3.1 above. It's the same code.

### code-solutions.py

Contains solutions to the function exercises:

1. greet_friends -- iterates over a list and prints a greeting for each name:

```python
friend_list = ["John", "Jane", "Jack"]

def greet_friends(friends):
    for friend in friends:
        print(f"Hello {friend}!")

greet_friends(friend_list)
```

2. calculate_tax -- takes income and tax_rate, returns the product:

```python
def calculate_tax(income, tax_rate):
    return income * tax_rate

print(calculate_tax(50000, 0.2))
```

3. compound_interest -- the full implementation with input validation and year-by-year calculation as described in Exercise 1.4.
