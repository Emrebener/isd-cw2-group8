from controllers import TaskManagerController
from tasks import TaskFactory
import datetime
class CommandLineUI:

    def _print_menu(self) -> None:
        print("To-Do List Manager") 
        print("1. Add a task") 
        print("2. View tasks") 
        print("3. Select a task")
        print("4. Import tasks")
        print("5. Export tasks")
        print("q. Quit")
  
    def run(self) -> None:
        name = input("Enter your name: ")
        self.controller = TaskManagerController(name)
        load_default = input("Would you like to load a default task list? (y/n): ")
        if load_default == "y":
            # print all files in the current directory
            self.controller.load_tasks("tasks.csv")
        
        while True:
            self._print_menu()
            choice = input("Enter your choice: ")
            if choice == "1":
                title = input("Enter a task: ")
                input_date = input("Enter a due date (YYYY-MM-DD): ")
                date_object = datetime.datetime.strptime(input_date, "%Y-%m-%d")

                while True:
                    reccuring = input("Is this a reccuring task? (y/n): ")
                    if reccuring == "y":
                        interval = int(input("Enter the interval between each repetition (days): "))

                        task = TaskFactory.create_task(title, date_object, interval=datetime.timedelta(days=interval))
                        break
                    elif reccuring == "n":
                        task = TaskFactory.create_task(title, date_object)
                        break
                    else:
                        print("Invalid choice.")
                
                self.controller.add_task(task)

            elif choice == "2":
                ix_tasks = self.controller.get_all_tasks()
                for ix, task in ix_tasks:
                    print(f"{ix} : {task}")
            elif choice == "3":
                ix = int(input("Enter the index of the task you wish to select: "))
                if self.controller.task_list.check_task_index(ix):
                    print(f"Selected task: {self.controller.task_list.get_task(ix)}")
                else:
                    print("Invalid index.")
                    continue
                
                while True:
                    print("1. Remove task")
                    print("2. Edit task")
                    print("3. Mark as complete")
                    print("q. Quit")
                    choice = input("Enter your choice: ")
                    if choice == "1":
                        self.controller.remove_task(ix)
                        break
                    elif choice == "2":
                        print("1. Change title")
                        print("2. Change due date")
                        choice = input("Enter your choice: ")
                        if choice == "1":
                            title = input("Enter a new title: ")
                            self.controller.task_list.get_task(ix).change_title(title)
                        elif choice == "2":
                            input_date = input("Enter a new due date (YYYY-MM-DD): ")
                            date_object = datetime.datetime.strptime(input_date, "%Y-%m-%d")
                            self.controller.task_list.get_task(ix).change_date_due(date_object)
                        else:
                            print("Invalid choice.")
                        break
                    elif choice == "3":
                        self.controller.complete_task(ix)
                        break
                    elif choice == "q":
                        break
                    else:
                        print("Invalid choice.")          
            elif choice == "4":
                task_path = input("Enter the path to the task file: ")
                try:
                    self.controller.load_tasks(task_path)
                except FileNotFoundError:
                    print("File not found, please try again.")  
            elif choice == "5":
                task_path = input("Enter the path to save the task file: ")
                try:
                    self.controller.save_tasks(task_path)
                except FileNotFoundError:
                    print("File not found, please try again.")
            elif choice == "q":
                break
        



                

        