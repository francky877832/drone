class Delivery:
    def __init__(self, id, pos, weight, priority, time_window):
        self.id = id
        self.pos = pos
        self.weight = weight
        self.priority = priority
        self.time_window = time_window  # ("HH:MM", "HH:MM")

    def is_within_time(self, current_time_str):
        from datetime import datetime
        fmt = "%H:%M"
        start = datetime.strptime(self.time_window[0], fmt)
        end = datetime.strptime(self.time_window[1], fmt)
        current = datetime.strptime(current_time_str, fmt)
        return start <= current <= end

    def __repr__(self):
        return f"<Delivery #{self.id} - {self.weight}kg - priority {self.priority}>"
