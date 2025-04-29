import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from data.events_data import events
from services.search_service import search_by_event_type, search_by_mood, search_by_time, search_by_artist
from services.filters import filter_by_location, filter_by_time_range, filter_by_today
from services.auto_save import save_last_search, load_last_search, save_search_to_csv

def display_event(event):
    print(event)
    print("-" * 40)

def main():
    print("\n✨ Welcome to Scene Scout! ✨\n")
    print("Where do you want to vibe tonight?")
    
    last_search = load_last_search()
    if last_search:
        print("Found your last search! Want to pick it up again? (y/n)")
        resume = input().strip().lower()
        if resume == 'y':
            filtered_events = last_search
        else:
            filtered_events = events
    else:
        filtered_events = events
    
    location = input("Choose location (Lavington / Westlands / Both): ").strip()
    if location.lower() != "both":
        filtered_events = filter_by_location(filtered_events, location)

    event_type = input("What type of event? (DJ Set / Live Music / Rooftop Party / Comedy / Art Show / Brunch Party): ").strip()
    if event_type:
        filtered_events = search_by_event_type(filtered_events, event_type)

    mood = input("What's your mood? (Hype / Chill / Relaxed / Romantic / Cultural): ").strip()
    if mood:
        filtered_events = search_by_mood(filtered_events, mood)

    artist = input("Any artist in mind? (Leave empty to skip): ").strip()
    if artist:
        filtered_events = search_by_artist(filtered_events, artist)


    print("\nFound the following events:\n")
    for event in filtered_events:
        display_event(event)

    print("Do you want to save this search? (y/n):")
    save_choice = input().strip().lower()
    if save_choice == 'y':
        save_last_search(filtered_events)
        save_search_to_csv(filtered_events)  

    
if __name__ == "__main__":
    main()
