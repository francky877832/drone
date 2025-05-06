import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from algorithms.a_star import a_star
from utils.data_generator import generate_scenario
from algorithms.graph import euclidean_distance
from utils.geometry import crosses_no_fly_zone

class TestAStar(unittest.TestCase):
    def setUp(self):
        # Set up the data for drones, deliveries, and no-fly zones
        self.num_drones = 3
        self.num_deliveries = 5
        self.num_zones = 2
        self.drones, self.deliveries, self.no_fly_zones = generate_scenario(self.num_drones, self.num_deliveries, self.num_zones)

        # Create a simple graph where nodes are deliveries
        self.delivery_graph = {}
        for delivery in self.deliveries:
            self.delivery_graph[delivery.id] = {}
            for other in self.deliveries:
                if delivery.id != other.id:
                    self.delivery_graph[delivery.id][other.id] = euclidean_distance(delivery.pos, other.pos)

    def test_a_star(self):
        # Select a start position (you can use the position of a drone or other)
        start_pos = self.drones[0].start_pos
        goal_id = self.deliveries[2].id  # Set the goal as the 3rd delivery point

        # Run A* to find the optimal path from start to goal
        path, cost = a_star(start_pos, self.deliveries, self.delivery_graph, goal_id, self.no_fly_zones)

        # Test if the path is not None and if the cost is valid
        self.assertIsNotNone(path, "No path found!")
        self.assertGreater(len(path), 0, "The path should have at least one point")
        print(f"Path: {path}, Cost: {cost}")

if __name__ == "__main__":
    unittest.main()
