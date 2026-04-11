scales = ["C", "F", "K"]

def convert(temperature_scale:str = "C", temperature_input:str = "0"):
    if scales.index(temperature_scale) == 0:  # Celsius
        degree_celcius = float(temperature_input)
        degree_fahrenheit = (degree_celcius * 9/5) + 32
        degree_kelvin = degree_celcius + 273.15
    elif scales.index(temperature_scale) == 1:  # Fahrenheit
        degree_fahrenheit = float(temperature_input)
        degree_celcius = (degree_fahrenheit - 32) * 5/9
        degree_kelvin = (degree_fahrenheit + 459.67) * 5/9
    elif scales.index(temperature_scale) == 2:  # Kelvin
        degree_kelvin = float(temperature_input)
        degree_celcius = degree_kelvin - 273.15
        degree_fahrenheit = (degree_kelvin - 273.15) * 9/5 + 32
    return degree_celcius, degree_fahrenheit, degree_kelvin

if __name__ == "__main__":
    temperature_scale = ("Enter the temperature scale you want to convert from: \n 'C' Celcius \n 'F' Fahrenheit \n 'K'. Kelvin \n")
    temperature_scale = input(temperature_scale).strip().upper()
    if temperature_scale not in scales:
        print("Invalid scale. Please enter 'C', 'F', or 'K'.")
        exit()
    temperature_input = input(f"Enter the temperature in {temperature_scale}: ")

    degree_celcius, degree_fahrenheit, degree_kelvin = convert(temperature_scale, temperature_input)

    print("Temperature Conversion Results:")
    print(f"{degree_celcius} degree Celsius")
    print(f"{degree_fahrenheit} degree Farenheit")
    print(f"{degree_kelvin} degree Kelvin")
    print("Thank you for using the Temperature Converter!")