import math
import matplotlib.pyplot as plt
import pandas as pd
import json
import os

'''
Object One: Hi-Flier XL
Object Two: Black Brant II
Object Three: Alpha Rocket
'''


# Constants
g = 9.81  # gravitational acceleration (m/s^2)
air_density = 1.225  # air density at sea level (kg/m^3)
drag_coefficient = 0.75  # drag coefficient (assumed)
rocket_mass = 0.1284  # mass of the rocket (kg)
propellant_mass = 12.4 / 1000 # mass of propellant (kg)
engine_thrust = 8  # average engine thrust of the engine (N)
burn_time = 0.8  # engine burn time (seconds)
total_impulse = 10  # total impulse (Ns)
diameter = 0.042  # diameter of the rocket (m)



def csv_reader(filepath, g = None):
    file = pd.read_csv(filepath)
       
    g_list = []
   
    rocket_mass = file["rocket_mass"]
    propellant_mass = file["propellant_mass"]
    engine_thrust = file["engine_thrust"]
    burn_time = file["burn_time"]
    total_impulse = file["total_impulse"]
    diameter = file["diameter"]
    drag_coefficient = file["drag_coefficient"]
    air_density = file["air_density"]
   
    if g != None:
        for i in range(len(rocket_mass)):
            g_list.append[g]
    else:
        g_list = file["g"]
   
    return [rocket_mass, propellant_mass, engine_thrust, burn_time, total_impulse, diameter, drag_coefficient,
            air_density, g_list]
   




def json_reader(filename):
    with open(filename, "r") as file:
        loaded_file = json.load(file)
    return loaded_file
 
 
   
def json_interpreter(file):
    rocket_dict = []
   
    for i in range(1, file.get("total_objects")):
        print(file.get(f"rocket:{i}"))
       
        frozen_set = frozenset(file.get(f"rocket:{i}").items())
        rocket_dict.append(frozen_set)
   
   
    print(rocket_dict)
    return rocket_dict



def converted_json_object_selecter(converted_file, requested_object):
   
    return converted_file[requested_object]
   




def json_creator(rocket_mass, propellant_mass, engine_thrust, burn_time, total_impulse, diameter,
                drag_coefficient, air_density, g):
                   
    old_data = {}
    count = 1

    if os.path.exists("rocket_stats.json"):
        old_data = json_reader("rocket_stats.json")
       
        existing_keys = [key for key in old_data.keys() if key.startswith("rocket:")]
        existing_numbers = [int(key.split(":")[1]) for key in existing_keys]
       
        if existing_numbers:
            count = max(existing_numbers) + 1

    data = {
        "rocket_mass": rocket_mass,
        "propellant_mass": propellant_mass,
        "engine_thrust": engine_thrust,
        "burn_time": burn_time,
        "total_impulse": total_impulse,
        "diameter": diameter,
        "drag_coefficient": drag_coefficient,
        "air_density": air_density,
        "gravity": g,
        "object_number": count
    }

    old_data[f"rocket:{count}"] = data
    old_data["total_objects"] = count

    with open("rocket_stats.json", "w") as json_file:
        json.dump(old_data, json_file, indent=2)

   
json_creator(rocket_mass, propellant_mass, engine_thrust, burn_time, total_impulse, diameter,
            drag_coefficient, air_density, g)

def rocket_objects_creation(rocket_mass, propellant_mass, engine_thrust, burn_time, total_impulse, diameter,
                            drag_coefficient, air_density, g):

    for i in range(len(rocket_mass)):
        json_creator(rocket_mass[i], propellant_mass[i], engine_thrust[i], burn_time[i], total_impulse[i],
        diameter[i], drag_coefficient[i], air_density[i], g[i])


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
    Vb = burnout_velocity_Fehskens_Malewicki_equations(rocket_mass, thrust, burn_time, diameter, g,
                                                        air_density, drag_coefficient)
   
    # Frontal Area
    A = math.pi * (diameter / 2) ** 2
   
    k =  0.5 * air_density * 0.75 * A
   
    # Burnout Altitude
    Yb = -(mass / (2 * k)) * math.log((thrust - mass*g - k * Vb**2) / (thrust - mass*g))

    print("Burnout Altitude: ", Yb, "m")
   
    return Yb
   
   
   
def coast_altitude_Fehskens_Malewicki_equations(rocket_mass, propellant_mass, thrust, burn_time, diameter, g,
                                                air_density, Cd):
    # Drag Coefficient
    if Cd == None:
        Cd = 0.75
       
    # burnout mass
    Mb = rocket_mass - propellant_mass
   
    #burnout Velocity
    Vb = burnout_velocity_Fehskens_Malewicki_equations(rocket_mass, thrust, burn_time, diameter,
                                                        g, air_density, drag_coefficient)
   
    # Frontal Area
    A = math.pi * (diameter / 2) ** 2
   
    k =  0.5 * air_density * 0.75 * A
   
    # Coast Altitude
    Yc = (Mb / (2 * k)) * math.log((Mb * g + k * Vb**2) / (Mb * g))
       
    print("Coast Altitude: ", Yc, "m")
   
    return Yc
   
   
   
   

burnout_velocity_Fehskens_Malewicki_equations(rocket_mass, engine_thrust, burn_time, diameter,
                                            g, air_density, drag_coefficient)

Yb = burnout_altitude_Fehskens_Malewicki_equations(rocket_mass, engine_thrust, burn_time,
                                                    diameter, g, air_density, drag_coefficient)

Yc = coast_altitude_Fehskens_Malewicki_equations(rocket_mass, propellant_mass, engine_thrust, burn_time,
                                                diameter, g, air_density, drag_coefficient)

print("Apogee:", Yb + Yc)

temp = json_reader("rocket_stats.json")

print(temp.get("rocket_mass"))

json_interpreter(json_reader("rocket_stats.json"))

print("Selected list", converted_json_object_selecter(json_interpreter(json_reader("rocket_stats.json")), 1))

testing_json = list(converted_json_object_selecter(json_interpreter(json_reader("rocket_stats.json")), 2))

print("Testing Rocket_Mass: ", next(v for k, v in testing_json if k == "rocket_mass"))

#Testing stuff
g = 9.81  # gravitational acceleration (m/s^2)
air_density = 1.225  # air density at sea level (kg/m^3)
drag_coefficient = 0.75  # drag coefficient (assumed)
rocket_mass = next(v for k, v in testing_json if k == "rocket_mass")  # mass of the rocket (kg)
propellant_mass = next(v for k, v in testing_json if k == "propellant_mass") # mass of propellant (kg)
engine_thrust = next(v for k, v in testing_json if k == "engine_thrust")  # average engine thrust of the engine (N)
burn_time = next(v for k, v in testing_json if k == "burn_time")  # engine burn time (seconds)
total_impulse = next(v for k, v in testing_json if k == "total_impulse")  # total impulse (Ns)
diameter = next(v for k, v in testing_json if k == "diameter")  # diameter of the rocket (m)

print("Look at this List Below: \n")

burnout_velocity_Fehskens_Malewicki_equations(rocket_mass, engine_thrust, burn_time, diameter,
                                            g, air_density, drag_coefficient)

Yb = burnout_altitude_Fehskens_Malewicki_equations(rocket_mass, engine_thrust, burn_time,
                                                    diameter, g, air_density, drag_coefficient)

Yc = coast_altitude_Fehskens_Malewicki_equations(rocket_mass, propellant_mass, engine_thrust, burn_time,
                                                diameter, g, air_density, drag_coefficient)

print("Apogee:", Yb + Yc)



def graph_rocket_performance(mass, propellant_mass, thrust, burn_time, diameter, g, air_density, Cd):
    import numpy as np
    import matplotlib.pyplot as plt

    A = math.pi * (diameter / 2)**2
    k = 0.5 * air_density * Cd * A
    avg_mass = (mass + (mass - propellant_mass)) / 2
    burnout_mass = mass - propellant_mass

    # Compute burnout velocity and altitudes
    Vb = burnout_velocity_Fehskens_Malewicki_equations(mass, thrust, burn_time, diameter, g, air_density, Cd)
    Yb = burnout_altitude_Fehskens_Malewicki_equations(mass, thrust, burn_time, diameter, g, air_density, Cd)
    Yc = coast_altitude_Fehskens_Malewicki_equations(mass, propellant_mass, thrust, burn_time, diameter, g, air_density, Cd)

    apogee_time = burn_time + (math.atan(Vb * math.sqrt(k / (burnout_mass * g))) * burnout_mass) / math.sqrt(burnout_mass * g * k)

    # Time arrays
    t_boost = np.linspace(0, burn_time, 500)
    t_coast = np.linspace(burn_time, apogee_time, 500)
    t_total = np.concatenate((t_boost, t_coast))

    # Altitude during boost
    alt_boost = []
    for t in t_boost:
        velocity = math.sqrt((thrust - avg_mass * g) / k) * math.tanh((t / avg_mass) * math.sqrt(k * (thrust - avg_mass * g)))
        altitude = -(avg_mass / (2 * k)) * math.log((thrust - avg_mass * g - k * velocity**2) / (thrust - avg_mass * g))
        alt_boost.append(altitude)

    # Altitude during coast
    alt_coast = []
    for t in t_coast:
        tc = t - burn_time
        velocity = Vb / (math.sqrt(1 + (Vb**2 * k * tc**2) / (burnout_mass**2)))
        altitude = Yb + (burnout_mass / (2 * k)) * math.log((burnout_mass * g + k * Vb**2) / (burnout_mass * g + k * velocity**2))
        alt_coast.append(altitude)

    altitude = np.concatenate((alt_boost, alt_coast))

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(t_total, altitude, label='Altitude (m)')
    plt.axvline(burn_time, linestyle='--', color='gray', label='Burnout')
    plt.axhline(Yb + Yc, linestyle=':', color='green', label='Apogee')
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.title("Rocket Altitude Over Time (Fehskens-Malewicki)")
    plt.legend()
    plt.grid(True)
    plt.show()
   
   
def test_graph_method(mass, propellant_mass, thrust, burn_time, diameter, g, air_density, Cd):
    
    
   
    '''  
    for i in range(len(rocket_mass)):
        json_creator(rocket_mass[i], propellant_mass[i], engine_thrust[i], burn_time[i], total_impulse[i], diameter[i],
            drag_coefficient[i], air_density[i], g[i])

    print("Apogee:", Yb + Yc)

    temp = json_reader("rocket_stats.json")

    print(temp.get("rocket_mass"))

    json_interpreter(json_reader("rocket_stats.json"))

    print("Selected list", converted_json_object_selecter(json_interpreter(json_reader("rocket_stats.json")), 1))
    '''

graph_rocket_performance(rocket_mass, propellant_mass, engine_thrust, burn_time, diameter, g, air_density, drag_coefficient)