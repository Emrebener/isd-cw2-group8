class User:                                                                
    def __init__(self, name: str, email: str):
        self.name = name                                                   
        self.email = email                                               
                                            
    def __str__(self) -> str:                                              
        return f"User: {self.name} ({self.email})"
                                                                            
                                                                        
class Owner(User):                           
    def __init__(self, name: str, email: str):
        super().__init__(name, email)

    def __str__(self) -> str:                                              
        return f"Owner: {self.name} ({self.email})"
                                                                    