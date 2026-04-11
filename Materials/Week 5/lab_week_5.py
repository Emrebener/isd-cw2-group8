"""
        Vehicle
    /           \
    Car             Plane
    / \              /    \
Electric Petrol Propeller  Jet 
"""

class Vehicle:
    def __init__(self, color, weight, max_speed, max_range=None, seats=None):
        self.color = color
        self.weight = weight
        self.max_speed = max_speed
        self.max_range = max_range
        self.seats = seats

    def move(self, speed):
        print(f"The vehicle is moving at {speed} km/h")

class Car(Vehicle):
    def __init__(self, color, weight, max_speed, form_factor, **kwargs):
        super().__init__(color, weight, max_speed, **kwargs)
        self.form_factor = form_factor

    def move(self, speed):
        print(f"The car is driving at {speed} km/h")

class Plane(Vehicle):
    def __init__(self, color, weight, max_speed, wingspan, **kwargs):
        super().__init__(color, weight, max_speed, **kwargs)
        self.wingspan = wingspan

    def move(self, speed):
        print(f"The plane is flying at {speed} km/h")

class Electric(Car):
    def __init__(self, color, weight, max_speed, form_factor, battery_capacity, **kwargs):
        super().__init__(color, weight, max_speed, form_factor, **kwargs)
        self.battery_capacity = battery_capacity

    def move(self, speed):
        print(f"The electric car is driving at {speed} km/h and has a maximum range of {self.max_range} km")

class Petrol(Car):
    def __init__(self, color, weight, max_speed, form_factor, fuel_capacity, **kwargs):
        super().__init__(color, weight, max_speed, form_factor, **kwargs)
        self.fuel_capacity = fuel_capacity

    def move(self, speed):
        print(f"The petrol car is driving at {speed} km/h")

class Propeller(Plane):
    def __init__(self, color, weight, max_speed, wingspan, propeller_diameter, **kwargs):
        super().__init__(color, weight, max_speed, wingspan, **kwargs)
        self.propeller_diameter = propeller_diameter

    def move(self, speed):
        print(f"The propeller plane is flying at {speed} km/h")

class Jet(Plane):
    def __init__(self, color, weight, max_speed, wingspan, engine_thrust, **kwargs):
        super().__init__(color, weight, max_speed, wingspan, **kwargs)
        self.engine_thrust = engine_thrust

    def move(self, speed):
        print(f"The jet plane is flying at {speed} km/h")

class FlyingCar(Car, Plane):
    def __init__(self, color, weight, max_speed, form_factor, wingspan, **kwargs):
        # we need to add the wingspan to the keyword arguments so that following the MRO, the Plane class gets all the keyword arguments it needs
        super().__init__(color, weight, max_speed, form_factor=form_factor, wingspan=wingspan, **kwargs)

    def move(self, speed):
        print(f"The flying car is driving at {speed} km/h")

electric_car = Electric("green", 1200, 200, "Hatchback", 100)
electric_car.move(100)

petrol_car = Petrol("red", 1500, 250, "SUV", 50)
petrol_car.move(150)

generic_vehicle = Vehicle("red", 1000, 200)
generic_vehicle.move(100)


generic_electric_car = Electric("red", 1000, 200, "SUV", 100, max_range=500, seats=5)
generic_electric_car.move(100)
print(generic_electric_car.seats)

generic_plane = Plane("red", 1000, 200, 100, seats=50)



generic_flying_car = FlyingCar("red", 1000, 200, "SUV", 30, seats=5)
generic_flying_car.move(100)
print(generic_flying_car.seats, generic_flying_car.wingspan, generic_flying_car.form_factor)


generic_flying_car_2 = FlyingCar(color="red", weight=1000, max_speed=200, form_factor="SUV", wingspan=30, seats=5)
generic_flying_car_2.move(100)

class Animal:
    # we omit the __init__ method for brevity
    
    def move(self, speed):
        print(f"The animal is moving at a speed of {speed}")

generic_animal = Animal()
generic_animal.move(20)





for movable_object in [generic_vehicle, generic_electric_car, generic_flying_car, generic_animal]:
    movable_object.move(20)