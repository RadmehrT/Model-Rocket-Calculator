import math
import matplotlib.pyplot as plt
import json

# Constants
g = 9.81  # gravitational acceleration (m/s^2)
air_density = 1.225  # air density at sea level (kg/m^3)
drag_coefficient = 0.75  # drag coefficient (assumed)
rocket_mass = 0.1448  # mass of the rocket (kg)
engine_thrust = 12.5  # updated maximum thrust of the engine (N)
burn_time = 1.6  # engine burn time (seconds)
total_impulse = 20  # total impulse (Ns)
diameter = 0.041656  # diameter of the rocket (m)

def json_creator(rocket_mass, engine_thrust, burn_time, total_impulse, diameter, drag_coefficient, air_density, g):
    
    data = {
        "rocket_mass": rocket_mass,
        "engine_thrust": engine_thrust,
        "burn_time": burn_time,
        "total_impulse": total_impulse,
        "diameter": diameter,
        "drag_coefficient": drag_coefficient,
        "air_density": air_density,
        "gravity": g
    }
    
    
    with open("rocket_stats.json", "w") as json_file:
        json.dump(data, json_file, indent=2)
    
json_creator(rocket_mass, engine_thrust, burn_time, total_impulse, diameter, drag_coefficient, air_density, g)

def json_reader(filename):
    with open(filename, "r") as file:
        loaded_file = json.load(file)
    return loaded_file

temp = json_reader("rocket_stats.json")

print(temp.get("rocket_mass"))

#Fehskens-Malewicki equations
def burnout_velocity_Fehskens_Malewicki_equations(mass, thrust, burn_time, diameter, g, air_density, Cd):
    # Drag Coefficient
    if Cd == None:
        Cd = 0.75
        
    averageMass = (mass + (mass - 24.2 / 1000)) / 2
    
    mass = averageMass
       
    # Frontal Area
    A = math.pi * (diameter / 2) ** 2
   
    k =  0.5 * air_density * 0.75 * A
   
    # Burnout Velocity
    Vb = math.sqrt( (thrust - (mass * g)) / k) * math.tanh( (burn_time / mass) * math.sqrt(k * (thrust - (mass * g))))
    print("burnout velolicty: ", Vb, "m/s")
   
def burnout_altitude_Fehskens_Malewicki_equations(mass, thrust, burn_time, diameter, g, air_density, Cd):
    # Drag Coefficient
    if Cd == None:
        Cd = 0.75
       
    averageMass = (mass + (mass - 24.2 / 1000)) / 2
    
    mass = averageMass
    
    # Frontal Area
    A = math.pi * (diameter / 2) ** 2
   
    k =  0.5 * air_density * 0.75 * A
   
    # Burnout Altitude
    Yb = (mass / k) * math.log(math.cosh(burn_time / mass) * math.sqrt(k * (thrust - (mass * g))))
    print("Burnout Altitude: ", Yb, "m")
   

burnout_velocity_Fehskens_Malewicki_equations(rocket_mass, engine_thrust, burn_time, diameter, g, air_density, drag_coefficient)

burnout_altitude_Fehskens_Malewicki_equations(rocket_mass, engine_thrust, burn_time, diameter, g, air_density, drag_coefficient)