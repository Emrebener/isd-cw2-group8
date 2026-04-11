unit = input("Enter the unit to convert from (C, K, or F): ")
value = float(input("Enter the temperature value: "))                      

if unit == "C":                                                            
    degree_f = value * 9/5 + 32                                          
    degree_k = value + 273.15                                              
    print(f"{value} Celsius is equal to {degree_f} Fahrenheit.")
    print(f"{value} Celsius is equal to {degree_k} Kelvin.")               
elif unit == "F":                                                        
    degree_c = (value - 32) * 5/9                                          
    degree_k = degree_c + 273.15                                         
    print(f"{value} Fahrenheit is equal to {degree_c} Celsius.")           
    print(f"{value} Fahrenheit is equal to {degree_k} Kelvin.")          
elif unit == "K":                                                          
    degree_c = value - 273.15
    degree_f = degree_c * 9/5 + 32                                         
    print(f"{value} Kelvin is equal to {degree_c} Celsius.")             
    print(f"{value} Kelvin is equal to {degree_f} Fahrenheit.")            
else:
    print("Invalid unit. Please enter C, K, or F.")     