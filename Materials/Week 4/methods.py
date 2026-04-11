class TaskList:
    def __init__(self, title):
        self.title = title

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, ix):
        del self.tasks[ix]

    def view_tasks(self):
        for ix, task in enumerate(self.tasks):
            print(f"{ix}: {task}")

    def list_options(self):                                                    
      while True:                                                            
          print("To-Do List Manager")                                        
          print("1. Add a task")                                             
          print("2. View tasks")               
          print("3. Remove a task")                                          
          print("4. Quit")                                                 
                                               
          choice = input("Enter your choice: ")                              
   
          if choice == "1":                                                  
            title = input("Enter a task: ")
            task = Task(title)
            self.add_task(task)          

          elif choice == "2":
            self.view_tasks()

          elif choice == "3":                                                
            ix = int(input("Enter the index of the task to remove: "))
            self.remove_task(ix)                                           
                                                                           
          elif choice == "4":                  
            break

my_task_list = TaskList("YOUR NAME")
my_task_list.tasks = ["Do Homework", "Do Laundry", "Go Shopping"]
my_task_list.list_options()