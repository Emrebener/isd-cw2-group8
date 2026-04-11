tasks = []

def add_task(list):
    list.appnd(input("Add a task: "))
    # list.append(input("Add a task: "))

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