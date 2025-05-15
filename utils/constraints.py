from shapely.geometry import LineString, Polygon
from models.drone import Drone
from models.delivery import Delivery
from models.no_fly_zone import NoFlyZone
from utils.helpers import euclidean_distance, estimate_arrival_time, is_within_time_window


from datetime import datetime, timedelta






def check_single_delivery_per_trip(drone):
  return drone.is_available()

def check_drone_recharging(drone) : 
    return drone.is_recharging

def check_drone_can_support_cost(drone, needed_cost):
    return drone.battery >= needed_cost

def check_drone_can_support_weigth(drone, delivery):
    return drone.max_weight >= delivery.weight

def check_drone_is_within_time_window(estimated_arrival_time, delivery):
     return is_within_time_window(estimated_arrival_time, delivery.time_window)


def check_all_csp(start, goal, drone, delivery, needed_cost):
    #cCSP CHECKIMG BEOFRE ASSIGNATION
    estimated_arrival_time = estimate_arrival_time(drone.start_time, euclidean_distance(start.pos, goal.pos), drone.speed) 

    if  check_single_delivery_per_trip(drone) and not check_drone_recharging(drone) :
        if check_drone_can_support_cost(drone, needed_cost):
            if check_drone_can_support_weigth(drone, delivery) :
                if check_drone_is_within_time_window(estimated_arrival_time, delivery):
                    return drone 
                else:
                    print(f"CSP Violation 4 - Drone {drone.id} arrival time is not with time window for Delivery {delivery.id}. {estimated_arrival_time} not in {delivery.time_window}  Re-adding to queue.")
            else:
                    print(f"CSP Violation 3 - Drone {drone.id} max_weight {drone.max_weight} under Delivery {delivery.id} weight {delivery.weight}. Re-adding to queue.")
                    
        else:
              print(f"CSP Violation 2 - Drone {drone.id} doesn't have enough battery for Delivery {delivery.id}. Re-adding to queue.")
    else:
        print(f"CSP Violation 1 -  Drone {drone.id} is not available. Re-adding to queue.")
        #csp4 - no fkyzone, penality is added
    return None
    



def check_all_csp_for_violation(start, goal, drone, delivery, needed_cost):
    #cCSP CHECKIMG BEOFRE ASSIGNATION
    estimated_arrival_time = estimate_arrival_time(drone.start_time, euclidean_distance(start.pos, goal.pos), drone.speed) 
    violations = 0
    if  not check_single_delivery_per_trip(drone) and not check_drone_recharging(drone) :
        violations += 1
    if not check_drone_can_support_cost(drone, needed_cost):
        violations += 1
    if not check_drone_can_support_weigth(drone, delivery) :
        violations += 1
    if not check_drone_is_within_time_window(estimated_arrival_time, delivery):
        violations += 1

    return violations
        