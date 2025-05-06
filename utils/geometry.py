from shapely.geometry import LineString, Polygon

def crosses_no_fly_zone(p1, p2, no_fly_zones):
    """
    Check if the line from p1 to p2 crosses any no-fly zone.
    """
    line = LineString([p1, p2])
    for zone in no_fly_zones:
        polygon = Polygon(zone.coordinates)
        if line.intersects(polygon):
            return True
    return False
