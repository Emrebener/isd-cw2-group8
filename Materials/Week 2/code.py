# Initialize an empty list to store tasks 
# TODO: Add code here to initialize an empty list 
tasks = []

 
# Function to add a task to the list 
def add_task(task): 
    # TODO: Add code here to add a task to the list 
    tasks.append(task)
    # Don't forget to add arguments to the function, if needed 

# Function to view current tasks in the list 
def view_tasks(): 
    # TODO: Add code here to view all tasks in the list 
    for ix, task in enumerate(tasks):
        print(ix, task)

# Function to remove a task from the list 
def remove_task(ix): 
    del tasks[ix]
 
# Main program loop 
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
