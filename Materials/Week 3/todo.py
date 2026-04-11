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