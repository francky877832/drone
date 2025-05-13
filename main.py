import json
import random
import time
import heapq
from models.drone import Drone
from models.delivery import Delivery
from models.no_fly_zone import NoFlyZone
from algorithms.graph_builder import build_graph, generate_complete_graph, generate_sparse_graph, generate_oriented_sparse_graph
from ga.population import generate_initial_population, generate_initial_full_population

from ga.ga import crossover, mutate, tournament_selection, generate_next_generation
from ga.fitness import evaluate_individual
from algorithms.a_start import a_star
from graphics.graph import plot_graph, plot_path, plot_combined_graph_and_path, plot_oriented_graph, plot_combined_oriented_graph_and_path
from utils.simulate_delivery import simulate_all, simulate_for_signle_delivery
from utils.helpers import initialize_drones_on_graph


#başlangıç zamanı alinmasi
start_time = time.time()

#scenario dosyasi açma ve data alınması
with open("scenario1.json", "r") as f:
    data = json.load(f)

#data : drone, delivery ve noflyzone nesnelerini kurmak
drones = [Drone(**d) for d in data["drones"]]
deliveries = [Delivery(**d) for d in data["deliveries"]]
no_fly_zones = [NoFlyZone(**z) for z in data["no_fly_zones"]]
population_size = len(drones)

#drones, grafta initialisation
initialize_drones_on_graph(deliveries, drones)


""" graph oluçturma, 4 tane graflerimiz var : normal bir graphe, complete bir graph, oriented and non oriented sparse graph"""
#rastlanti_graph = build_graph(drones[0].start_pos, deliveries)
#graph = generate_complete_graph(deliveries)
#graph = generate_oriented_sparse_graph(deliveries, 3)
graph = generate_sparse_graph(deliveries, 3)

"""graf gosterisi"""
#plot_graph(deliveries, graph, no_fly_zones)


"""A_start calişması ve path çizgisi"""
"""
#kaynak, hedef and seçilen drone. Sadece deneyim için
start = deliveries[16]
goal = deliveries[19]
drone = drones[2]

#A_start en ucuz path bulmanın gosterisi : bulundugun path'in 2 nokta arasında buyuk bir maliyet verilir ve o path'tan daha ucuz olan bulur
#node1 = deliveries[17]
#node2 = deliveries[2]
#graph[tuple(node1.pos)][tuple(node2.pos)] = 12000000

path = a_star(graph, start, goal, no_fly_zones, drone, deliveries)
plot_combined_graph_and_path(deliveries, graph, no_fly_zones, path)
"""

"""GA CSP CALISMASI"""

print("\nBaşlangıc nufus uretme...")
population_size = 10
population = generate_initial_full_population(drones, deliveries, size=population_size)

def check_empty_population(population):
    for idx, individu in enumerate(population):
        if all(len(livraisons) == 0 for livraisons in individu.values()):
            print(f"Birey {idx + 1}: Hiçbir drone'a teslimat atanmamış. Yebi bir senaryo seciniz.")
            exit()
"""baslanıc nufus bos olma kontrolü"""
check_empty_population(population)


"""GA çalışmasi"""
best_individuals = []
number_generation = 2
# Generation sayısına kadra GA yurutulmesi, 1 genration = bir iterasiyon
for generation in range(number_generation):
    print(f"Generation {generation+1}")
    
    # Bir nufus icin fitness hesaplama
    population_fitness = [(individual, evaluate_individual(individual, graph, no_fly_zones, drones, deliveries)) for individual in population]
    
    # Mevcut nufustan en iyi individu alınmasi (elitism)
    best_individual = max(population_fitness, key=lambda x: x[1])
    print(f"Best individual: {best_individual[0]} => {best_individual[1]}")

    #Tum nufus en iyi individu dizisine kaydetmek
    best_individuals.append(best_individual)
    
    # Bir dahaki generation uretme
    population = generate_next_generation(population, graph, no_fly_zones, drones, deliveries)


#Tum Generation en iyilerinin en iyisi alınmak
best_individual = max(best_individuals, key=lambda x : x[1])
print(f"\nBEST INDIVIDUAL AMONG ALL GENERATION : {best_individual[0]} => {best_individual[1]}.\n")

#En iyi individu teslimatlarinı alinmak, bir minHeap içinde
best_deliveries = [d for d in deliveries for i in best_individual[0].values() if d.id in i]
delivery_heap = []
for delivery in best_deliveries:
    heapq.heappush(delivery_heap, (-delivery.priority, delivery)) #heappop en kucuk element veriyor, o yuzden delivery.priority yerine -delivery.priority kullanılır


#Her teslimatin path'larini saklanmak icin
plot_path = []

#Bu dongu icerseinde, en iyi teslimatlari rotalarini bulmaya calısır,
for i in range(len(delivery_heap)) :
    delivery = heapq.heappop(delivery_heap) #heappop en buyuk mutlak degri olan veriyor
    delivery = delivery[1] # cunku bu sekilde saklandı : (-delivery.priority, delivery)

    for drone_id, delivery_list in best_individual[0].items():
        if delivery.id in delivery_list:
            assigned_drone = drone_obj = next((d for d in drones if f"D{d.id}" == drone_id), None)
            break
    path = simulate_for_signle_delivery(graph, assigned_drone, delivery, deliveries, no_fly_zones)
    plot_path.append(path)
    
    print("\n")

#Algorithma'nın bitme zamanı
end_time = time.time()


print(f"Verimlilik :  {end_time-start_time} seconds.\n")

#butun bulundugu rotalar gosterme
#print(plot_path)
for path in plot_path :
    plot_combined_graph_and_path(deliveries, graph, no_fly_zones, path)