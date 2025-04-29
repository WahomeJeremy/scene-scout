def search_by_event_type(events, event_type):
    return [event for event in events if event.event_type.lower() == event_type.lower()]

def search_by_mood(events, mood):
    return [event for event in events if event.mood.lower() == mood.lower()]

def search_by_time(events, preferred_time):
    return [event for event in events if event.start_time.startswith(preferred_time)]

def search_by_artist(events, artist_name):
    return [event for event in events if artist_name.lower() in event.performer.lower()]

