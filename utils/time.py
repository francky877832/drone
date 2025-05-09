def is_within_time_window(now, start, end):
    return start <= now <= end


from datetime import datetime, timedelta

def generate_time_slots(start="09:00", interval_minutes=10, count=10):
    fmt = "%H:%M"
    current = datetime.strptime(start, fmt)
    slots = []

    for _ in range(count):
        if current.hour >= 24:
            break  # Arrêter si on dépasse 23:59
        slot_start = current.strftime(fmt)
        current += timedelta(minutes=interval_minutes)
        if current.hour >= 24:
            break
        slot_end = current.strftime(fmt)
        slots.append([slot_start, slot_end])
    
    return slots


