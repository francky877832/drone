import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def plot_graph(deliveries, graph, no_fly_zones):
    fig, ax = plt.subplots()

    # Tracer les zones interdites
    for i, zone in enumerate(no_fly_zones):
        poly = Polygon(zone.coordinates)
        x, y = poly.exterior.xy
        label = 'No-Fly Zone' if i == 0 else None  # Éviter les doublons dans la légende
        ax.fill(x, y, color='red', alpha=0.3, label=label)

    # Préparer un dictionnaire d'accès rapide aux positions
    id_to_pos = {d.id: d.pos for d in deliveries}

    # Tracer les points de livraison
    for dp in deliveries:
        ax.plot(dp.pos[0], dp.pos[1], 'bo')  # blue dots
        ax.text(dp.pos[0]+1, dp.pos[1]+1, f'{dp.id}', fontsize=8)

    # Tracer les arêtes du graphe
    for from_pos, neighbors in graph.items():
        #from_pos = id_to_pos[from_id]
        for to_pos in neighbors:
            #to_pos = id_to_pos[to_id]
            ax.plot([from_pos[0], to_pos[0]],
                    [from_pos[1], to_pos[1]],
                    'gray', linewidth=0.5)

    ax.set_title("Graph des livraisons avec zones interdites")
    ax.set_xlabel("X (mètres)")
    ax.set_ylabel("Y (mètres)")
    ax.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()


import matplotlib.pyplot as plt

def plot_path(path, deliveries) :
    x_coords, y_coords = zip(*path)
    

    # Création du graphique
    plt.figure(figsize=(10, 10))
    plt.plot(x_coords, y_coords, marker='o', color='b', label='Chemin', linestyle='-', markersize=8)

    # Ajouter des flèches pour la direction
    for i in range(len(path) - 1):
        x_start, y_start = path[i]
        x_end, y_end = path[i + 1]

        plt.arrow(x_start, y_start, x_end - x_start, y_end - y_start, 
                head_width=3, head_length=5, fc='r', ec='r')

    # Marquer les points sur le graphe
    for (x, y) in path:
        d_id = next((d.id for d in deliveries if tuple(d.pos) == (x, y)), None)
        plt.text(x, y, f'{d_id}-({x}, {y})', fontsize=9, ha='right')

    # Paramètres d'affichage
    plt.title("Visualisation du chemin avec direction")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()

    # Affichage du chemin
    plt.show()