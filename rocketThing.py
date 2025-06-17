import math
import matplotlib.pyplot as plt
import json

# Constants
g = 9.81  # gravitational acceleration (m/s^2)
air_density = 1.225  # air density at sea level (kg/m^3)
drag_coefficient = 0.75  # drag coefficient (assumed)
rocket_mass = 0.1448  # mass of the rocket (kg)
propellant_mass = 45.6 / 1000 # mass of propellant (kg)
engine_thrust = 12.5  # updated maximum thrust of the engine (N)
burn_time = 1.6  # engine burn time (seconds)
total_impulse = 20  # total impulse (Ns)
diameter = 0.041656  # diameter of the rocket (m)

def json_creator(rocket_mass, propellant_mass, engine_thrust, burn_time, total_impulse, diameter, drag_coefficient, air_density, g):
    
    data = {
        "rocket_mass": rocket_mass,
        "propellant mass": propellant_mass,
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
    
json_creator(rocket_mass, propellant_mass, engine_thrust, burn_time, total_impulse, diameter, drag_coefficient, air_density, g)

def json_reader(filename):
    with open(filename, "r") as file:
        loaded_file = json.load(file)
    return loaded_file




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
    print("burnout velocity: ", Vb, "m/s")
    
    return Vb
   
   
   
   
   
def burnout_altitude_Fehskens_Malewicki_equations(mass, thrust, burn_time, diameter, g, air_density, Cd):
    # Drag Coefficient
    if Cd == None:
        Cd = 0.75
       
    averageMass = (mass + (mass - 24.2 / 1000)) / 2
    
    mass = averageMass
    
    #burnout Velocity
    Vb = burnout_velocity_Fehskens_Malewicki_equations(rocket_mass, thrust, burn_time, diameter, g, air_density, drag_coefficient)
    
    # Frontal Area
    A = math.pi * (diameter / 2) ** 2
   
    k =  0.5 * air_density * 0.75 * A
   
    # Burnout Altitude
    Yb = -(mass / (2 * k)) * math.log((thrust - mass*g - k * Vb**2) / (thrust - mass*g))

    print("Burnout Altitude: ", Yb, "m")
    
    return Yb
   
   
   
def coast_altitude_Fehskens_Malewicki_equations(rocket_mass, propellant_mass, thrust, burn_time, diameter, g, air_density, Cd):
    # Drag Coefficient
    if Cd == None:
        Cd = 0.75
        
    # burnout mass
    Mb = rocket_mass - propellant_mass
    
    #burnout Velocity
    Vb = burnout_velocity_Fehskens_Malewicki_equations(rocket_mass, thrust, burn_time, diameter, g, air_density, drag_coefficient)
    
    # Frontal Area
    A = math.pi * (diameter / 2) ** 2
   
    k =  0.5 * air_density * 0.75 * A
   
    # Coast Altitude
    Yc = (Mb / (2 * k)) * math.log((Mb * g + k * Vb**2) / (Mb * g))
        
    print("Coast Altitude: ", Yc, "m")
    
    return Yc

burnout_velocity_Fehskens_Malewicki_equations(rocket_mass, engine_thrust, burn_time, diameter, g, air_density, drag_coefficient)

Yb = burnout_altitude_Fehskens_Malewicki_equations(rocket_mass, engine_thrust, burn_time, diameter, g, air_density, drag_coefficient)

Yc = coast_altitude_Fehskens_Malewicki_equations(rocket_mass, propellant_mass, engine_thrust, burn_time, diameter, g, air_density, drag_coefficient)

print("Apogee: ", Yb + Yc)

temp = json_reader("rocket_stats.json")

print(temp.get("rocket_mass"))
