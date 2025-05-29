from shapely.geometry import Point, Polygon
from datetime import datetime

class NoFlyZone:
    def __init__(self, id, coordinates, active_time, violable=True):
        self.id = id
        self.coordinates = coordinates  # liste de (x, y)
        self.active_time = active_time  # ("HH:MM", "HH:MM")
        self.polygon = Polygon(coordinates)  # Polygone oluşturuluyor
        self.violable = violable

    """def is_active(self, current_time_str):
        from datetime import datetime
        fmt = "%H:%M"
        start = datetime.strptime(self.active_time[0], fmt)
        end = datetime.strptime(self.active_time[1], fmt)
        current = datetime.strptime(current_time_str, fmt)
        return start <= current <= end"""
    
    def is_active(self, current_time_str):
        fmt = "%H:%M"
        current = datetime.strptime(current_time_str, fmt)
        start = datetime.strptime(self.active_time[0], fmt)
        end = datetime.strptime(self.active_time[1], fmt)

        if start <= end:
            return start <= current <= end
        else:
            return current >= start or current <= end


    def contains(self, pos):
        return self.polygon.contains(Point(pos))  # Nokta bölgenin içinde mi?

    def __repr__(self):
        return f"<NoFlyZone #{self.id} - aktif {self.active_time}>"
