import json
import requests

# Toffee Playlist Source
SOURCE_URL = "https://raw.githubusercontent.com/srhady/toffee-bd/refs/heads/main/toffee_playlist.json"

# আপনি যে চ্যানেল চান
TARGET_CHANNEL_NAME = "Zee Bangla"

def update_channel_m3u8():
    try:
        response = requests.get(SOURCE_URL, timeout=10)
        response.raise_for_status()
        playlist = response.json()

        target_url = None
        logo_url = ""
        matched_name = TARGET_CHANNEL_NAME

        # ১. প্লেলিস্ট থেকে Zee Bangla বা কাছাকাছি নাম খোঁজা (Case-insensitive)
        # স্পেস বা ড্যাশ বাদ দিয়েও সার্চ করবে
        target_clean = TARGET_CHANNEL_NAME.lower().replace(" ", "").replace("-", "")

        for item in playlist:
            channel_name = item.get("name") or item.get("title") or ""
            clean_name = channel_name.lower().replace(" ", "").replace("-", "")

            if target_clean in clean_name:
                target_url = item.get("link") or item.get("url")
                logo_url = item.get("logo") or item.get("logo_url") or ""
                matched_name = channel_name
                break

        # ২. যদি কোনো কারণে চ্যানেল না পাওয়া যায়, তবে ফাইল যেন খালি না থাকে (ফেলসেফ)
        if not target_url and len(playlist) > 0:
            print(f"Warning: '{TARGET_CHANNEL_NAME}' not found directly. Falling back to available item.")
            target_url = playlist[0].get("link") or playlist[0].get("url")
            logo_url = playlist[0].get("logo") or playlist[0].get("logo_url") or ""

        if target_url:
            # M3U8 Playlist তৈরি
            m3u8_content = "#EXTM3U\n"
            m3u8_content += f'#EXTINF:-1 tvg-logo="{logo_url}",{matched_name}\n'
            m3u8_content += f"{target_url}\n"

            # ফাইল রাইট করা
            with open("playlist.m3u8", "w", encoding="utf-8") as f:
                f.write(m3u8_content)

            with open("stream.txt", "w", encoding="utf-8") as f:
                f.write(target_url)

            print(f"Successfully generated files for: {matched_name}")
            print(f"URL: {target_url}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_channel_m3u8()
