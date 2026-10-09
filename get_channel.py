import json
import requests

# Toffee Playlist Source
SOURCE_URL = "https://raw.githubusercontent.com/srhady/toffee-bd/refs/heads/main/toffee_playlist.json"

# আপনার কাঙ্ক্ষিত চ্যানেলের নাম (যেমন: "Somoy TV", "ATN Bangla", "T Sports" ইত্যাদি)
TARGET_CHANNEL_NAME = "Zee Bangla"

def update_channel_link():
    try:
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        playlist = response.json()

        target_url = None

        # প্লেলিস্ট থেকে চ্যানেলটি খোঁজা
        for item in playlist:
            if TARGET_CHANNEL_NAME.lower() in item.get("name", "").lower():
                target_url = item.get("link") or item.get("url")
                break

        if target_url:
            # লিংক পাওয়ার পর তা channel_link.txt ফাইলে সেভ করা
            with open("channel_link.txt", "w", encoding="utf-8") as f:
                f.write(target_url)
            print(f"Successfully saved link for {TARGET_CHANNEL_NAME}")
        else:
            print(f"Channel '{TARGET_CHANNEL_NAME}' not found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_channel_link()
