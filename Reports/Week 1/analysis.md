# Week 1 -- Introduction to Python Programming I

**Module:** COMP11124 Object Oriented Programming  
**Materials:** `Week1.pdf`, `lab_week_1.py`

---

## Exercise 0: Installing Python

This one's straightforward -- just downloading and installing the Python interpreter from the official site. Nothing to code here, but it's the foundation for everything else since we need the interpreter to actually run any Python scripts.

---

## Exercise 1: Setting Up Visual Studio Code

Again, mostly setup. We install VS Code as our code editor and open the provided `lab_week_1.py` file. VS Code prompts you to install the Python extension on first launch, which you should accept -- it gives you syntax highlighting, IntelliSense, and that handy play button to run scripts.

The starter file already has some code in it:

```python
print("Hello. Welcome to the OOP Module.")
print("This program has been run successfully.")

class_name = "OOP"
number_of_students = 20
my_string = "Welcome to the " + class_name + " module. There are " + str(number_of_students) + " students in this class."

my_string = f"Welcome to the {class_name} module. There are {number_of_students} students in this class."
```

We're asked to run this and change the `name` variable to see how the output changes. The code shows two ways of building a string from variables -- concatenation with `+` (where you have to manually call `str()` on non-string types) and f-strings (where you just drop variables inside `{}` and Python handles the rest). Both produce the same output, but the f-string version is much cleaner.

---

## Exercise 2: Running a Script Using the Command Line

This exercise shows that you don't need VS Code's play button to run Python. You can open a terminal (CMD on Windows, Terminal on Mac), navigate to where your file is saved with `cd`, and run it with:

```
python lab_week_1.py
```

The output is the same either way. The point is that there are multiple ways to execute Python code, and knowing how to use the command line is a useful skill on its own.

---

## Exercise 1 (Section 2): Variables and Types

Now we actually start coding. This exercise is about understanding Python's basic data types and how to check and convert between them.

We're given four variables and asked to guess their types:

| Variable | Value | Type |
|----------|-------|------|
| `var_1` | `True` | `bool` |
| `var_2` | `1` | `int` |
| `var_3` | `3.14159` | `float` |
| `var_4` | `"Hello World"` | `str` |

To verify, we use `print(type(var_1))` and so on. The `type()` function is really handy for debugging when you're not sure what kind of data you're working with.

Then comes **casting** -- converting values from one type to another. Python gives us `int()`, `float()`, `str()`, and `bool()` for this. Some important things to note:

- `float(5)` gives `5.0` -- no data is lost going from int to float.
- `int(5.5)` gives `5` -- it truncates (chops off the decimal), it doesn't round.
- `int(True)` gives `1` -- booleans map to integers where `True` is `1` and `False` is `0`.

The exercise has us create variables, cast them, and observe the results. It's a good way to build intuition about how Python handles types behind the scenes.

---

## Exercise 2 (Section 2): Arithmetic Operators

This covers all seven arithmetic operators Python offers:

| Operator | Symbol | Example | Result |
|----------|--------|---------|--------|
| Addition | `+` | `10 + 5` | `15` |
| Subtraction | `-` | `20 - 8` | `12` |
| Multiplication | `*` | `6 * 4` | `24` |
| Division | `/` | `15 / 3` | `5.0` |
| Floor Division | `//` | `17 // 4` | `4` |
| Modulus | `%` | `17 % 4` | `1` |
| Exponentiation | `**` | `2 ** 3` | `8` |

One thing worth noting: `/` always returns a float in Python 3, even if the result is a whole number (so `15 / 3` gives `5.0`, not `5`). If you want an integer result, use `//` for floor division instead.

We also see that `print()` can take multiple arguments separated by commas, like `print("Addition:", result_addition)`, which prints them with a space in between.

After understanding the operators, we apply them to two practical tasks:

- **Calculating an average:** Create two numbers and compute `(num1 + num2) / 2`.
- **Area of a rectangle:** Create `length` and `width` variables and compute `length * width`.

These are simple but they get you used to combining variables and operators to solve actual problems.

---

## Exercise 3 (Section 2): Strings and f-Strings

This exercise goes deeper into strings. We already saw basic string usage, but now we learn that strings in Python are objects with built-in methods we can call.

**String methods we're asked to use:**

- `.upper()` -- converts the entire string to uppercase
- `.lower()` -- converts the entire string to lowercase
- `.replace(old, new)` -- swaps out part of the string for something else
- `len(string)` -- returns how many characters are in the string (this is a built-in function, not a method, so it's called as `len(my_string)` rather than `my_string.len()`)

The exercise also emphasizes reading documentation -- we're pointed to the W3Schools Python string reference and expected to figure out how to use these methods ourselves. That's an important skill; you're never going to memorize every function in a language, so knowing how to look things up matters.

Then comes the **f-strings** section. We've already seen these in the starter code, but now we get to create our own. We make variables for our name, number of classes, and campus, and combine them into a sentence like:

```python
my_text = f"My name is {my_name} and I am studying {number_of_classes} classes in {campus}."
```

Compared to concatenation, f-strings handle type conversion automatically and are way easier to read. Once you start using them, you don't really go back.

---

## Exercise (Section 3): Temperature Converter

This is the final exercise and it brings everything together. We write a complete program that converts a Celsius temperature to Fahrenheit and Kelvin.

**What we need to do:**

1. Store a Celsius value in `celsius_input`
2. Convert to Fahrenheit using the formula: `degree_f = celsius_input * 9/5 + 32`
3. Convert to Kelvin using the formula: `degree_k = celsius_input + 273.15`
4. Print the results using f-strings in a specific format

**Expected output (for an input of 25):**

```
Welcome to the Temperature Converter!

The temperature you have entered is 25 degree Celsius.

Converted Temperatures:
25 degree Celsius is equal to 77.0 Fahrenheit.
25 degree Celsius is equal to 298.15 Kelvin.

Thank you for using the Temperature Converter!
```

This exercise uses variables (to store the input and results), arithmetic operators (for the conversion formulas), and f-strings (for the formatted output). It's a nice synthesis of everything covered in the week.

---

## Closing Thoughts

Week 1 is purely procedural -- no functions, no classes, no control flow (if/else, loops). Even though the module is called "Object Oriented Programming," it makes sense to start here since all the OOP concepts in later weeks will build on these fundamentals: variables, types, operators, and basic string handling.
