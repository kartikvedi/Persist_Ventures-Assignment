import googlemaps
import requests
import os
import time
import random
from dotenv import load_dotenv

# Load environment variables for sensitive information
load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
SUNO_API_ENDPOINT = "https://api.suno.ai/v1"
LOGIN_ENDPOINT = f"{SUNO_API_ENDPOINT}/auth/login"
GENERATE_MUSIC_ENDPOINT = f"{SUNO_API_ENDPOINT}/music/generate"
DOWNLOAD_SONG_ENDPOINT = f"{SUNO_API_ENDPOINT}/music/download"

# Login credentials for Suno API
LOGIN_CREDENTIALS = {
    "Google": {"username": "your_google_username", "password": "your_google_password"},
    "Apple": {"username": "your_apple_username", "password": "your_apple_password"},
    "Discord": {"username": "your_discord_username", "password": "your_discord_password"}
}

# Set up multiple accounts for switching
ACCOUNTS = [
    {"username": "account1_username", "password": "account1_password"},
    {"username": "account2_username", "password": "account2_password"}
]

# Set up music generation prompts
PROMPTS = ["calm road trip vibes", "upbeat travel beats", "relaxing campfire tunes"]

class AskEmily:
    def __init__(self, rv_type, rv_height, rv_length):
        self.gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        self.rv_type = rv_type
        self.rv_height = rv_height
        self.rv_length = rv_length

    def recommend_trip(self, start, destination):
        directions = self.gmaps.directions(start, destination, mode="driving", avoid="tolls")
        if directions:
            route_info = directions[0]["legs"][0]
            distance = route_info["distance"]["text"]
            duration = route_info["duration"]["text"]
            print(f"Route from {start} to {destination}: Distance - {distance}, Duration - {duration}")
            return f"Recommended route from {start} to {destination} added."
        else:
            return "No route found. Please check your locations."

    def get_gps_route(self):
        bridge_clearance_alert = (
            "Bridge clearance of 14 ft ahead" if self.rv_height < 14 else "Clear route ahead."
        )
        return {
            "route": "Custom Route for RV",
            "bridge_alert": bridge_clearance_alert
        }

class SunoMusic:
    def __init__(self):
        self.current_account_index = 0
        self.current_account = ACCOUNTS[self.current_account_index]

    def login(self, login_option):
        login_credentials = LOGIN_CREDENTIALS[login_option]
        for attempt in range(5):
            response = requests.post(LOGIN_ENDPOINT, json={"username": login_credentials["username"], 
                                                            "password": login_credentials["password"]})
            if response.status_code == 200:
                return response.json().get("access_token")
            elif response.status_code == 503:
                print("Service unavailable, retrying...")
                time.sleep(2 ** attempt)
            else:
                print("Login failed:", response.text)
                return None
        print("Max retries reached. Unable to login.")
        return None

    def generate_music(self, access_token, prompt):
        headers = {"Authorization": f"Bearer {access_token}"}
        for attempt in range(5):
            response = requests.post(GENERATE_MUSIC_ENDPOINT, headers=headers, json={"prompt": prompt})
            if response.status_code == 200:
                return response.json()["song_id"]
            elif response.status_code == 503:
                print("Service unavailable while generating music, retrying...")
                time.sleep(2 ** attempt)
            else:
                print("Error generating music:", response.text)
                return None
        print("Max retries reached. Unable to generate music.")
        return None

    def download_song(self, access_token, song_id):
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(DOWNLOAD_SONG_ENDPOINT, headers=headers, params={"song_id": song_id})
        if response.status_code == 200:
            with open(f"song_{song_id}.mp3", "wb") as f:
                f.write(response.content)
            return True
        else:
            print("Error downloading song:", response.text)
            return False

    def switch_account(self):
        self.current_account_index = (self.current_account_index + 1) % len(ACCOUNTS)
        self.current_account = ACCOUNTS[self.current_account_index]

    def start_music_generation(self):
        while True:
            access_token = self.login("Google")
            if access_token is None:
                self.switch_account()
                continue

            prompt = random.choice(PROMPTS)
            song_id = self.generate_music(access_token, prompt)
            if song_id is None:
                self.switch_account()
                continue

            if not self.download_song(access_token, song_id):
                self.switch_account()
                continue

            print(f"Song generated and downloaded successfully using account {self.current_account['username']}!")
            time.sleep(2)  # Adjust time as needed


# Initializing Ask Emily
emily = AskEmily(rv_type="Class A", rv_height=13.5, rv_length=35)

# Example Usage:
print(emily.recommend_trip("San Francisco", "Los Angeles"))
print("GPS Route Info:", emily.get_gps_route())

# Initializing SunoMusic for music generation
suno_music = SunoMusic()
suno_music.start_music_generation()
