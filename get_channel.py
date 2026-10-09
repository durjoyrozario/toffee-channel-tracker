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

        for item in playlist:
            name = item.get("name") or item.get("title") or "Unknown Channel"
            url = item.get("link") or item.get("url") or item.get("stream_url") or ""
            logo = item.get("logo") or item.get("logo_url") or ""

            if url:
                m3u_content += f'#EXTINF:-1 tvg-logo="{logo}",{name}\n{url}\n\n'
                
                clean_key = name.lower().replace(" ", "").replace("-", "")
                channels_dict[clean_key] = {
                    "name": name,
                    "url": url,
                    "logo": logo
                }
    except Exception as e:
        print(f"Fetch error: {e}")

    # কোনো কারণে সোর্স লিংক না পেলেও অন্তত খালি না রেখে ফাইল সেভ করবে
    with open("playlist.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u_content)

    with open("channels.json", "w", encoding="utf-8") as f:
        json.dump(channels_dict, f, indent=4, ensure_ascii=False)

    print(f"Processed {len(channels_dict)} channels successfully!")

if __name__ == "__main__":
    update_channels()
