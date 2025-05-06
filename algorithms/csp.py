class CSP:
    def __init__(self, drones, deliveries, no_fly_zones):
        self.drones = drones
        self.deliveries = deliveries
        self.no_fly_zones = no_fly_zones
        self.constraints = []

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def is_valid(self, solution):
        for constraint in self.constraints:
            if not constraint(solution):
                return False
        return True

    def get_valid_assignments(self):
        """
        Génère toutes les affectations valides pour chaque drone.
        """
        valid_assignments = []
        for drone in self.drones:
            for delivery in self.deliveries:
                # Vérifie les contraintes ici
                if self.is_valid({drone: delivery}):
                    valid_assignments.append({drone: delivery})
        return valid_assignments

# Exemple de test
if __name__ == "__main__":
    class Drone:
        def __init__(self, drone_id, start_pos):
            self.drone_id = drone_id
            self.start_pos = start_pos

    class Delivery:
        def __init__(self, delivery_id, pos):
            self.delivery_id = delivery_id
            self.pos = pos

    drones = [Drone(1, (0, 0)), Drone(2, (5, 5))]
    deliveries = [Delivery(1, (2, 2)), Delivery(2, (8, 8))]

    csp = CSP(drones, deliveries, [])
    valid_assignments = csp.get_valid_assignments()
    print("Valid Assignments:", valid_assignments)
