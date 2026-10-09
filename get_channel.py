import json
import requests

# মূল প্লেলিস্টের লিংক
SOURCE_URL = "https://raw.githubusercontent.com/srhady/toffee-bd/refs/heads/main/toffee_playlist.json"

# আপনি যে চ্যানেলটির লিংক আলাদাভাবে ব্যাকগ্রাউন্ডে আপডেট করতে চান
TARGET_CHANNEL_NAME = "Zee Bangla" 

# আপনার কাঙ্ক্ষিত ফাইলের নাম (যেমন: zee-bangla.m3u8)
OUTPUT_FILENAME = "zee-bangla.m3u8"

def update_single_channel():
    try:
        response = requests.get(SOURCE_URL, timeout=10)
        response.raise_for_status()
        playlist = response.json()

        # যদি ডেটা ডাইরেক্ট লিস্ট না হয়ে কোনো অবজেক্টের ভেতরে থাকে
        if isinstance(playlist, dict):
            for key in ["channels", "data", "playlist", "items"]:
                if key in playlist and isinstance(playlist[key], list):
                    playlist = playlist[key]
                    break

        target_url = None
        logo_url = ""
        matched_name = TARGET_CHANNEL_NAME

        target_clean = TARGET_CHANNEL_NAME.lower().replace(" ", "").replace("-", "")

        # মূল লিস্ট থেকে নির্দিষ্ট চ্যানেলটি খোঁজা
        for item in playlist:
            if not isinstance(item, dict):
                continue
                
            name = str(item.get("name") or item.get("title") or item.get("channel_name") or "")
            clean_name = name.lower().replace(" ", "").replace("-", "")

            if target_clean in clean_name:
                target_url = item.get("link") or item.get("url") or item.get("stream_url") or item.get("file") or ""
                logo_url = item.get("logo") or item.get("logo_url") or item.get("img") or ""
                matched_name = name
                break

        # যদি লিংক পাওয়া যায়, তবে .m3u8 ফরম্যাটে ফাইল তৈরি করা
        if target_url:
            m3u8_content = f"#EXTM3U\n#EXTINF:-1 tvg-logo=\"{logo_url}\",{matched_name}\n{target_url}\n"
            
            with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
                f.write(m3u8_content)
                
            print(f"Successfully updated {OUTPUT_FILENAME} with live stream for {matched_name}!")
        else:
            print(f"Channel '{TARGET_CHANNEL_NAME}' not found in the source list.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_single_channel()
