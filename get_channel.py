import json
import requests

SOURCE_URL = "https://raw.githubusercontent.com/srhady/toffee-bd/refs/heads/main/toffee_playlist.json"

def update_channels():
    m3u_content = "#EXTM3U\n\n"
    channels_dict = {}

    try:
        response = requests.get(SOURCE_URL, timeout=10)
        response.raise_for_status()
        playlist = response.json()

        # যদি ডেটা ডাইরেক্ট লিস্ট না হয়ে কোনো অবজেক্টের ভেতরে থাকে
        if isinstance(playlist, dict):
            # সম্ভাব্য লিস্ট কি-গুলো চেক করা
            for key in ["channels", "data", "playlist", "items"]:
                if key in playlist and isinstance(playlist[key], list):
                    playlist = playlist[key]
                    break

        for item in playlist:
            if not isinstance(item, dict):
                continue
                
            # সব ধরনের সম্ভাব্য ফিল্ড নেম হ্যান্ডেল করার ব্যবস্থা
            name = item.get("name") or item.get("title") or item.get("channel_name") or "Unknown"
            url = item.get("link") or item.get("url") or item.get("stream_url") or item.get("file") or ""
            logo = item.get("logo") or item.get("logo_url") or item.get("img") or ""

            if url:
                m3u_content += f'#EXTINF:-1 tvg-logo="{logo}",{name}\n{url}\n\n'
                
                clean_key = str(name).lower().replace(" ", "").replace("-", "")
                channels_dict[clean_key] = {
                    "name": name,
                    "url": url,
                    "logo": logo
                }
    except Exception as e:
        print(f"Error: {e}")

    # ফাইল সেভ করা
    with open("playlist.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    with open("channels.json", "w", encoding="utf-8") as f:
        json.dump(channels_dict, f, indent=4, ensure_ascii=False)

    print(f"Total channels found: {len(channels_dict)}")

if __name__ == "__main__":
    update_channels()
