import requests
import json
import notify2
import os  # Import the 'os' module

# URL of the cache.json file here is 45
url = "https://download.gnome.org/core/46/46.3/cache.json"
# url = "https://download.gnome.org/core/44/44.5/cache.json"
# Path to the local database file i use the same folder tha script runs
db_file = "gnome46_3_cache_db.json"
# db_file = "gnome44_5_cache_db.json"
# Initialize notify2, notify2 its a dep
notify2.init("Webpage Monitor")

def load_previous_content():
    if os.path.exists(db_file):
        with open(db_file, "r") as file:
            return json.load(file)
    return None

def save_current_content(content):
    with open(db_file, "w") as file:
        json.dump(content, file)

response = requests.get(url)

if response.status_code == 200:
    current_content = json.loads(response.text)

    last_content = load_previous_content()

    if current_content != last_content:
        notification_title = "Webpage Updated!"
        notification_text = "The webpage has been updated."

        n = notify2.Notification(notification_title, notification_text)
        n.show()

        save_current_content(current_content)

        print("Webpage was updated.")
    else:
        print("Webpage was not updated.")
else:
    print("Failed to fetch the webpage.")

