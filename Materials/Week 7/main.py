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
                # create a new task object based on the title entered and the date entered
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

