class DeliveryPoint:
    def __init__(self, delivery_id, pos, weight, priority, time_window):
        self.id = delivery_id
        self.pos = pos                    # tuple (x, y)
        self.weight = weight              # in kg
        self.priority = priority          # 1 to 5
        self.time_window = time_window    # tuple ("HH:MM", "HH:MM")

        self.assigned = False

    def __repr__(self):
        return f"DeliveryPoint(id={self.id}, pos={self.pos}, weight={self.weight}kg, priority={self.priority})"
