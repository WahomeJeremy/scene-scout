class Event:
    def __init__(self, name, venue, performer, duration_hours, event_type, mood, tags):
        self.name = name
        self.venue = venue
        self.performer = performer
        self.duration_hours = duration_hours
        self.event_type = event_type
        self.mood = mood
        self.tags = tags

    def __str__(self):
        return (
            f"🎤 {self.name}\n"
            f"📍 Venue: {self.venue}\n"
            f"🎶 Performer: {self.performer}\n"
            f"🕗 Starts at: {self.start_time}\n"
            f"⏳ Duration: {self.duration_hours} hours\n"
            f"🎭 Type: {self.event_type}\n"
            f"🌟 Mood: {self.mood}\n"
            f"🏷️ Tags: {', '.join(self.tags)}\n"
        )
    

