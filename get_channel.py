import json
import requests

SOURCE_URL = "https://raw.githubusercontent.com/srhady/toffee-bd/refs/heads/main/toffee_playlist.json"

def update_channels():
    try:
        response = requests.get(SOURCE_URL, timeout=10)
        response.raise_for_status()
        playlist = response.json()

        m3u_content = "#EXTM3U\n\n"
        channels_dict = {}

        for item in playlist:
            name = item.get("name") or item.get("title") or ""
            url = item.get("link") or item.get("url") or item.get("stream_url") or ""
            logo = item.get("logo") or item.get("logo_url") or ""

            if name and url:
                # M3U8 প্লেলিস্ট ফরম্যাট
                m3u_content += f'#EXTINF:-1 tvg-logo="{logo}",{name}\n{url}\n\n'
                
                # সহজে খুঁজে পাওয়ার জন্য ডিকশনারি তৈরি
                clean_key = name.lower().replace(" ", "").replace("-", "")
                channels_dict[clean_key] = {
                    "name": name,
                    "url": url,
                    "logo": logo
                }

        # ১. মাস্টার প্লেলিস্ট ফাইল
        with open("playlist.m3u8", "w", encoding="utf-8") as f:
            f.write(m3u_content)

        # ২. সব চ্যানেলের লিঙ্কের JSON ফাইল
        with open("channels.json", "w", encoding="utf-8") as f:
            json.dump(channels_dict, f, indent=4, ensure_ascii=False)

        print("Successfully updated all channels!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_channels()
