def filter_by_location(events, location):
    return [event for event in events if location.lower() in event.venue.lower()]

def filter_by_time_range(events, start_time, end_time):
    return [event for event in events if start_time <= event.start_time <= end_time]

def filter_by_today(events):
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    return [event for event in events if today in event.start_time]
