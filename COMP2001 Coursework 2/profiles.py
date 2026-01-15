from flask import abort, make_response
import json
import os
from datetime import date, timedelta
import random

DATA_FILE = "profiles.json"

DATA = {
    "profiles": [],
    "preferences": [],
    "favourites": [],
    "activity_master": [
        {"activityID": 1, "name": "Trail Running", "description": "Running on off-road paths."},
        {"activityID": 2, "name": "Mountain Biking", "description": "Cycling through rugged terrains."},
        {"activityID": 3, "name": "Wild Camping", "description": "Staying overnight in the wilderness."},
        {"activityID": 4, "name": "Rock Climbing", "description": "Scaling natural rock formations."},
        {"activityID": 5, "name": "Bird Watching", "description": "Observing local wildlife."}
    ]
}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(DATA, f, indent=4)
    print("--- Data successfully saved to profiles.json ---")

def load_data():
    global DATA
    if os.path.exists(DATA_FILE):
        print(f"--- Loading existing data from {DATA_FILE} ---")
        with open(DATA_FILE, "r") as f:
            saved_data = json.load(f)
            # Ensure activity_master is always fresh from our definition
            saved_data["activity_master"] = DATA["activity_master"]
            DATA = saved_data
    else:
        print("--- No JSON file found. Creating default test data... ---")

        mandatory_accounts = [
            {"user": "Grace Hopper", "email": "grace@plymouth.ac.uk", "first": "Grace", "last": "Hopper", "loc": "Dartmoor"},
            {"user": "Tim Berners-Lee", "email": "tim@plymouth.ac.uk", "first": "Tim", "last": "Berners-Lee", "loc": "Plymouth"},
            {"user": "Ada Lovelace", "email": "ada@plymouth.ac.uk", "first": "Ada", "last": "Lovelace", "loc": "Snowdonia"}
        ]

        for entry in mandatory_accounts:
            username = entry["user"]

            def generate_random_birthday(min_age=18, max_age=70):
                today = date.today()
                start_date = today - timedelta(days=max_age * 365)
                end_date = today - timedelta(days=min_age * 365)
                days_between = (end_date - start_date).days
                random_days = random.randrange(days_between)
                random_birthday = start_date + timedelta(days=random_days)
                return random_birthday.strftime("%Y-%m-%d")

            DATA["profiles"].append({
                "username": username,
                "first_name": entry["first"],
                "last_name": entry["last"],
                "email": entry["email"],
                "phone": f"07{random.randint(100000000, 999999999)}",
                "about_me": "I am an randomly generated test account.",
                "location": entry["loc"],
                "height": random.randint(160, 190),
                "weight": random.randint(60, 90),
                "birthday": generate_random_birthday(13, 60)
            })

            DATA["preferences"].append({
                "username": username,
                "activity_time_preference": random.choice(["speed", "pace"]),
                "marketing_language": "English",
                "units": random.choice(["metric", "imperial"])
            })

            random_act = random.choice(DATA["activity_master"])
            DATA["favourites"].append({
                "username": username,
                "activityID": random_act["activityID"]
            })

        save_data()

# Initialize data when the module is imported
load_data()

def read_all():
    print("DEBUG: GET /profiles called")
    return DATA

def read_one(username):
    print(f"DEBUG: GET /profiles/{username} called")
    profile = next((p for p in DATA["profiles"] if p["username"] == username), None)
    if not profile:
        abort(404, f"Profile {username} not found")

    prefs = next((p for p in DATA["preferences"] if p["username"] == username), {})
    user_fav_ids = [f["activityID"] for f in DATA["favourites"] if f["username"] == username]
    detailed_favs = [act for act in DATA["activity_master"] if act["activityID"] in user_fav_ids]

    return {
        "details": profile,
        "preferences": prefs,
        "favourites": detailed_favs
    }

def create(body):
    username = body.get("username")
    print(f"DEBUG: Attempting to create user: {username}")

    if any(p["username"] == username for p in DATA["profiles"]):
        abort(406, f"User {username} already exists")

    new_profile = {
        "username": username,
        "first_name": body.get("first_name", ""),
        "last_name": body.get("last_name", ""),
        "email": body.get("email"),
        "phone": body.get("phone", ""),
        "about_me": body.get("about_me", ""),
        "location": body.get("location", "Unknown"),
        "height": body.get("height", 0),
        "weight": body.get("weight", 0),
        "birthday": body.get("birthday", "")
    }

    new_prefs = {
        "username": username,
        "activity_time_preference": body.get("activity_time_preference", "speed"),
        "marketing_language": body.get("marketing_language", "en"),
        "units": body.get("units", "metric")
    }

    random_act = random.choice(DATA["activity_master"])
    DATA["favourites"].append({
        "username": username,
        "activityID": random_act["activityID"]
    })

    DATA["profiles"].append(new_profile)
    DATA["preferences"].append(new_prefs)
    save_data()

    return {
        "details": new_profile,
        "preferences": new_prefs,
        "assigned_starter_activity": random_act["name"]
    }, 201

def update(username, body):
    print(f"DEBUG: Updating user: {username}")
    profile = next((p for p in DATA["profiles"] if p["username"] == username), None)
    prefs = next((p for p in DATA["preferences"] if p["username"] == username), None)

    if not profile:
        abort(404, f"User {username} not found")

    for key in ["first_name", "last_name", "email", "phone", "about_me", "location", "height", "weight", "birthday"]:
        if key in body:
            profile[key] = body[key]

    for key in ["activity_time_preference", "marketing_language", "units"]:
        if key in body:
            prefs[key] = body[key]

    save_data()
    return {"details": profile, "preferences": prefs}, 200

def delete(username):
    print(f"DEBUG: Deleting user: {username}")
    global DATA
    if not any(p["username"] == username for p in DATA["profiles"]):
        abort(404, f"User {username} not found")

    DATA["profiles"] = [p for p in DATA["profiles"] if p["username"] != username]
    DATA["preferences"] = [p for p in DATA["preferences"] if p["username"] != username]
    DATA["favourites"] = [f for f in DATA["favourites"] if f["username"] != username]

    save_data()
    return make_response(f"User {username} successfully deleted", 200)

def get_random_activity():
    return random.choice(DATA["activity_master"])