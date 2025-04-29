import pickle
import csv
import datetime
import json
import os

SAVE_FILE = 'last_search.pkl'
CSV_FILE_BASE = 'scene'  
PREFS_FILE = "user_prefs.json"

def load_prefs():
    if os.path.exists(PREFS_FILE):
        with open(PREFS_FILE, 'r') as f:
            return json.load(f)
    return {"dark_mode": False}

def save_prefs():
    with open(PREFS_FILE, 'w') as f:
        json.dump(USER_PREFS, f, indent=4)

USER_PREFS = load_prefs()

def save_last_search(events):
    with open(SAVE_FILE, 'wb') as f:
        pickle.dump(events, f)

def load_last_search():
    try:
        with open(SAVE_FILE, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

def save_search_to_csv(events):
    if not events:
        print("No events to save to CSV.")
        return

    event_dicts = []
    for event in events:
        if isinstance(event, dict):
            event_dicts.append(event)
        else:
            event_dicts.append(event.__dict__)

    if not event_dicts:
        print("No valid events to save.")
        return

    fieldnames = event_dicts[0].keys()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    csv_filename = f"{CSV_FILE_BASE}_{timestamp}.csv"

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(event_dicts)

    print(f"✅ Saved your search results to '{csv_filename}' successfully!")

def update_user_preferences(new_preferences):
    global USER_PREFS
    USER_PREFS.update(new_preferences)
    save_prefs()
    print("✅ Updated user preferences.")

