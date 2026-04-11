colours = ["red", "green", "blue"]
print(colours)
                                                                            
print(colours[1])  # green
                                                                            
colours[0] = "yellow"                                                    
print(colours)  # ["yellow", "green", "blue"]
                                                                            
print(len(colours))  # 3
                                                                            
if "red" in colours:                                                     
    print("Red is in the list")              
else:
    print("Red is not in the list")
                                                                            
selected_colours = colours[1:3]
print(selected_colours)  # ["green", "blue"]              