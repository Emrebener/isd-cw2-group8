from tasks import Task                                                     
from users import Owner                                                  
import datetime                              

class TaskList:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.tasks: list[Task] = []
                                                                            
    def get_task(self, ix: int) -> Task:
        return self.tasks[ix]                                              
                                                                        
    def add_task(self, task: Task) -> None:  
        self.tasks.append(task)

    def remove_task(self, ix: int) -> None:                                
        del self.tasks[ix]
                                                                            
    def view_tasks(self) -> None:                                        
        print(f"Task list for {self.owner}:")
        for ix, task in enumerate(self.tasks):
            print(f"{ix}: {task}")