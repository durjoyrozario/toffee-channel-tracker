import json
import requests

# Toffee Playlist Source URL
SOURCE_URL = "https://raw.githubusercontent.com/srhady/toffee-bd/refs/heads/main/toffee_playlist.json"

# আপনি যে চ্যানেলের m3u8 লিংক চান তার নাম (প্রয়োজন অনুযায়ী পরিবর্তন করুন)
TARGET_CHANNEL_NAME = "Zee Bangla"

def update_channel_m3u8():
    try:
        # মূল JSON ফাইলটি ফেচ করা
        response = requests.get(SOURCE_URL, timeout=10)
        response.raise_for_status()
        playlist = response.json()

        target_url = None
        logo_url = ""

        # প্লেলিস্টের ভেতরে নির্দিষ্ট চ্যানেলটি খোঁজা
        for item in playlist:
            channel_name = item.get("name") or item.get("title") or ""
            if TARGET_CHANNEL_NAME.lower() in channel_name.lower():
                target_url = item.get("link") or item.get("url")
                logo_url = item.get("logo") or item.get("logo_url") or ""
                break

        if target_url:
            # ১. M3U8 Playlist Format তৈরি
            m3u8_content = "#EXTM3U\n"
            m3u8_content += f'#EXTINF:-1 tvg-logo="{logo_url}",{TARGET_CHANNEL_NAME}\n'
            m3u8_content += f"{target_url}\n"

            # playlist.m3u8 ফাইলে রাইট করা
            with open("playlist.m3u8", "w", encoding="utf-8") as f:
                f.write(m3u8_content)

            # ২. শুধুমাত্র ডাইরেক্ট M3U8 URL-টি stream.txt ফাইলে রাইট করা
            with open("stream.txt", "w", encoding="utf-8") as f:
                f.write(target_url)

            print(f"Successfully updated files for: {TARGET_CHANNEL_NAME}")
            print(f"Stream URL: {target_url}")
        else:
            print(f"Error: Channel '{TARGET_CHANNEL_NAME}' not found in the source list.")

    except Exception as e:
        print(f"An error occurred while updating the playlist: {e}")

if __name__ == "__main__":
    update_channel_m3u8()
