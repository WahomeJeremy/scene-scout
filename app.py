# app.py (USSD App)
from flask import Flask, request
from data.events_data import events
from services.search_service import search_by_event_type, search_by_mood, search_by_time, search_by_artist
from services.filters import filter_by_location
from services.auto_save import save_search_to_csv
from send_sms import send_sms  # Import send_sms function from send_sms.py
import os
import africastalking

app = Flask(__name__)

# Initialize Africa's Talking API for SMS
username = 'sandbox'
api_key = 'atsk_9399b61cc1618bcaca93799482ba793a7cf3192f203b7751febf6aebd8504b16314f3585'
africastalking.initialize(username, api_key)

@app.route('/', methods=['GET', 'POST'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")

    user_response = text.strip().split("*")
    response = ""

    try:
        # STEP 0: Starting screen
        if text == "":
            response = "CON Scene Scout 🎭\nWhere do you want to vibe tonight?\n"
            response += "1. Lavington\n2. Westlands\n3. Both"

        # STEP 1: Location selection
        elif len(user_response) == 1:
            location_map = {"1": "Lavington", "2": "Westlands", "3": "Both"}
            location = location_map.get(user_response[0], "Both")
            response = "CON What type of event?\n1. DJ Set\n2. Live Music\n3. Rooftop Party\n4. Comedy\n5. Art Show\n6. Brunch Party"

        # STEP 2: Event type selection
        elif len(user_response) == 2:
            response = "CON What’s your mood?\n1. Hype\n2. Chill\n3. Relaxed\n4. Romantic\n5. Cultural"

        # STEP 3: Mood selection
        elif len(user_response) == 3:
            response = "CON Enter preferred artist name or type '0' to skip:"

        # STEP 4: Artist Name (Final Step)
        elif len(user_response) == 4:
            location_map = {"1": "Lavington", "2": "Westlands", "3": "Both"}
            type_map = {
                "1": "DJ Set", "2": "Live Music", "3": "Rooftop Party",
                "4": "Comedy", "5": "Art Show", "6": "Brunch Party"
            }
            mood_map = {
                "1": "Hype", "2": "Chill", "3": "Relaxed",
                "4": "Romantic", "5": "Cultural"
            }

            location = location_map.get(user_response[0], "Both")
            event_type = type_map.get(user_response[1], "")
            mood = mood_map.get(user_response[2], "")
            artist = user_response[3] if user_response[3] != "0" else ""
            start_time = user_response[4] if user_response[4] != "0" else ""

            # Apply filters cumulatively and handle empty lists
            filtered_events = events
            print(f"Initial events: {len(filtered_events)}")  # Debug: Initial event count

            # Apply location filter
            if location != "Both":
                filtered_events = filter_by_location(filtered_events, location)
                print(f"After filtering by location: {len(filtered_events)}")  # Debug: After location filter

            # Apply event type filter
            if event_type:
                filtered_events = search_by_event_type(filtered_events, event_type)
                print(f"After filtering by event type: {len(filtered_events)}")  # Debug: After event type filter

            # Apply mood filter
            if mood:
                filtered_events = search_by_mood(filtered_events, mood)
                print(f"After filtering by mood: {len(filtered_events)}")  # Debug: After mood filter

            # Apply artist filter
            if artist:
                filtered_events = search_by_artist(filtered_events, artist)
                print(f"After filtering by artist: {len(filtered_events)}")  # Debug: After artist filter

            # Apply time filter (if necessary)
            if start_time:
                filtered_events = search_by_time(filtered_events, start_time)
                print(f"After filtering by time: {len(filtered_events)}")  # Debug: After time filter

            # Check if any events were found
            if filtered_events:
                # Prepare to send top events via SMS
                event_names = ", ".join([e.title for e in filtered_events[:3]])  # Get top 3 events by title

                send_sms(event_names, phone_number)  # Send SMS to the user
                save_search_to_csv(filtered_events)  # Save search to CSV
                response = f"END We've sent the top events to your phone! Check your SMS."

            else:
                response = "END No events match your vibe. Try again later."

        else:
            response = "END Invalid input. Please start again."

    except Exception as e:
        response = f"END Something went wrong: {e}"

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
