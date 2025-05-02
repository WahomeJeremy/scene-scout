def filter_by_location(events, location):
    return [event for event in events if location.lower() in event.venue.lower()]


