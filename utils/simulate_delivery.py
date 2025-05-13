import heapq
from time import sleep
from utils.helpers import get_battery_needed, compute_cost, is_within_time_window, estimate_arrival_time, euclidean_distance
from algorithms.a_start import a_star
from utils.constraints import check_all_csp

from datetime import datetime, timedelta



def simulate_for_signle_delivery(graph, drone, delivery, deliveries, no_fly_zones):
  

    print(f"Simlation for delivery : {delivery.id} - priority : {delivery.priority} - drone : {drone.id} : {drone.start_pos}")

    available_drone = drone
    needed_cost = 0
    path = None
     
          
    #compute needed energy = cost
    start = next(d for d in deliveries if tuple(d.pos) == tuple(drone.start_pos))
    goal = next(d for d in deliveries if tuple(d.pos) == tuple(delivery.pos))
    
    #this cost already tookm in consideration the penality
    path = a_star(graph, start, goal, no_fly_zones, drone, deliveries)
    for i in range(len(path)-1) :
        needed_cost += graph[path[i]][path[i+1]]
        
    check_all_csp(start, goal, drone, delivery, needed_cost)



    # update drone before delivery
    available_drone.current_weight = delivery.weight #CSP 1 drone = 1 delivery

        # update drone after delivery
    available_drone.move(delivery.pos) #position

    available_drone.update_battery(needed_cost)
    delivery.complete() 


    available_drone.start_recharge(1000) #1000mA

        #start_time
    estimated_arrival_time = estimate_arrival_time(available_drone.start_time, euclidean_distance(start.pos, goal.pos), available_drone.speed) 
        
    arrival_time = datetime.strptime(estimated_arrival_time, "%H:%M")
    time_to_charge = timedelta(minutes=available_drone.recharge_time)
    time_to_deliver = timedelta(minutes=available_drone.current_weight*0.1) #estimation

    start_time = arrival_time + time_to_charge + time_to_deliver
    available_drone.start_time = start_time.strftime("%H:%M")

    available_drone.current_weight = 0
    available_drone.decrement_recharge_time()
    available_drone.is_recharging = False
    available_drone.carrying_weight = 0.0



    return path






def simulate_all(graph, drones, deliveries, no_fly_zones, delivery_heap):
    # Simulation - on itère tant qu'il y a des livraisons
    tick_count = 0
    max_ticks = 100  # Limite de temps pour éviter une boucle infinie
    while delivery_heap and tick_count < max_ticks:
        print(f"Tick: {tick_count}")


        #extracting hignhest priority delivery
        delivery = heapq.heappop(delivery_heap)

        print(f"Simlation for delivery : {delivery.id}")

        # Chercher un drone disponible
        available_drone = None
        needed_cost = 0
        path = None
        for drone in drones:
          
            #compute needed energy = cost
            start = next(d for d in deliveries if tuple(d.pos) == tuple(drone.start_pos))
            goal = next(d for d in deliveries if tuple(d.pos) == tuple(delivery.pos))
            path = a_star(graph, start, goal, no_fly_zones, drone, deliveries)
            #this cost already tookm in consideration the penality
            for i in range(len(path)-1) :
                needed_cost += graph[path[i]][path[i+1]]
        
            available_drone = check_all_csp(start, goal, drone, delivery, needed_cost)

            if available_drone is not None : #drone found among drones
                print(f"Assigning Delivery {delivery.id} to Drone {drone.id}")
                break

        if available_drone is None:
            print("No drone available. All drones are either recharging or in use.")
            heapq.heappush(delivery_heap, delivery)
            break

        # update drone before delivery
        available_drone.current_weight = delivery.weight #CSP 1 drone = 1 delivery

        # update drone after delivery
        available_drone.move(delivery.pos) #position

        available_drone.update_battery(needed_cost)
        delivery.complete() 


        available_drone.start_recharge(1000) #1000mA

        #start_time
        estimated_arrival_time = estimate_arrival_time(available_drone.start_time, euclidean_distance(start.pos, goal.pos), available_drone.speed) 
        
        arrival_time = datetime.strptime(estimated_arrival_time, "%H:%M")
        time_to_charge = timedelta(minutes=available_drone.recharge_time)
        time_to_deliver = timedelta(minutes=available_drone.current_weight*0.1) #estimation

        start_time = arrival_time + time_to_charge + time_to_deliver
        available_drone.start_time = start_time.strftime("%H:%M")

        available_drone.current_weight = 0
        drone.decrement_recharge_time()
        drone.is_available = True


        tick_count += 1

        return path

    if tick_count >= max_ticks:
        print("Simulation reached maximum ticks, stopping.")
