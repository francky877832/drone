class NoFlyZone:
    def __init__(self, zone_id, coordinates, active_time):
        self.id = zone_id
        self.coordinates = coordinates        # list of (x, y) tuples
        self.active_time = active_time        # tuple ("HH:MM", "HH:MM")

    def __repr__(self):
        return f"NoFlyZone(id={self.id}, active={self.active_time})"
