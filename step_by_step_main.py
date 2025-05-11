import matplotlib.pyplot as plt
from shapely.geometry import Polygon


import matplotlib.pyplot as plt
from shapely.geometry import Polygon



import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def plot_combined_graph_and_path(deliveries, graph, no_fly_zones, path):
    # Create a single figure and axis for both the graph and the path
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot no-fly zones
    for i, zone in enumerate(no_fly_zones):
        poly = Polygon(zone.coordinates)
        x, y = poly.exterior.xy
        label = 'No-Fly Zone' if i == 0 else None  # Avoid duplicate legend labels
        ax.fill(x, y, color='red', alpha=0.3, label=label)

    # Plot delivery points
    for dp in deliveries:
        ax.plot(dp.pos[0], dp.pos[1], 'bo')  # Blue dots for delivery points
        ax.text(dp.pos[0]+1, dp.pos[1]+1, f'{dp.id}', fontsize=8)

    # Plot the graph edges (connections) with arrows to show direction
    for from_pos, neighbors in graph.items():
        for to_pos in neighbors:
            # Draw edge as a line
            ax.plot([from_pos[0], to_pos[0]], [from_pos[1], to_pos[1]], color='gray', linewidth=0.5)
            
            # Add green arrow to indicate direction (very small)
            dx, dy = to_pos[0] - from_pos[0], to_pos[1] - from_pos[1]
            ax.arrow(from_pos[0], from_pos[1], dx * 0.1, dy * 0.1,  # Reduced scale for smaller arrows
                     head_width=1, head_length=1, fc='gray', ec='gray')

    # Plot the path over the graph
    if path:
        x_coords, y_coords = zip(*path)
        ax.plot(x_coords, y_coords, marker='o', color='green', label='Path', linestyle='-', markersize=8)

        # Add arrows to indicate path direction
        for i in range(len(path) - 1):
            x_start, y_start = path[i]
            x_end, y_end = path[i + 1]
            dx, dy = x_end - x_start, y_end - y_start
            ax.arrow(x_start, y_start, dx * 0.1, dy * 0.1,  # Reduced scale for smaller arrows
                     head_width=1, head_length=1, fc='gray', ec='gray')

        # Label path points with delivery ID and coordinates
        for (x, y) in path:
            d_id = next((d.id for d in deliveries if tuple(d.pos) == (x, y)), None)
            ax.text(x, y, f'{d_id}-({x}, {y})', fontsize=9, ha='right')

    # Axis and legend settings
    ax.set_title("Graph with Path and No-Fly Zones")
    ax.set_xlabel("X (meters)")
    ax.set_ylabel("Y (meters)")
    ax.legend()
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')
    plt.show()



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

    # Tracer les arêtes du graphe avec des flèches pour indiquer la direction
    for from_pos, neighbors in graph.items():
        for to_pos in neighbors:
            # Tracer l'arête
            ax.plot([from_pos[0], to_pos[0]], [from_pos[1], to_pos[1]], 'gray', linewidth=0.5)

            # Ajouter une flèche pour indiquer la direction
            dx, dy = to_pos[0] - from_pos[0], to_pos[1] - from_pos[1]
            ax.arrow(from_pos[0], from_pos[1], dx * 0.1, dy * 0.1,  # Réduire l'échelle pour des flèches petites
                     head_width=1, head_length=1, fc='gray', ec='gray')

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



