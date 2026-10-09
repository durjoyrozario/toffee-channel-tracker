import json
import requests
import re

SOURCE_URL = "https://raw.githubusercontent.com/srhady/toffee-bd/refs/heads/main/toffee_playlist.json"

def clean_filename(name):
    # ফাইলের নামের জন্য অকার্যকর ক্যারেক্টার সরানো
    clean_name = re.sub(r'[\/:*?"<>| ]+', '_', name).strip('_').lower()
    return clean_name

def update_all_channels():
    try:
        response = requests.get(SOURCE_URL, timeout=10)
        response.raise_for_status()
        playlist = response.json()

        m3u_content = "#EXTM3U\n\n"
        all_channels_data = []

        for item in playlist:
            name = item.get("name") or item.get("title") or "Unknown"
            url = item.get("link") or item.get("url") or item.get("stream_url")
            logo = item.get("logo") or item.get("logo_url") or ""

            if not url:
                continue

            # ১. মাস্টার M3U8 প্লেলিস্ট তৈরি
            m3u_content += f'#EXTINF:-1 tvg-logo="{logo}",{name}\n{url}\n\n'

            # ২. প্রতিটি চ্যানেলের জন্য আলাদা টেক্সট ফাইল তৈরি (যেমন: somoy_tv.txt, zee_bangla.txt)
            file_name = f"{clean_filename(name)}.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(url)

            all_channels_data.append({
                "name": name,
                "stream_url": url,
                "logo": logo,
                "file_name": file_name
            })

        # মাস্টার ফাইলগুলো সেভ করা
        with open("playlist.m3u8", "w", encoding="utf-8") as f:
            f.write(m3u_content)

        with open("channels.json", "w", encoding="utf-8") as f:
            json.dump(all_channels_data, f, indent=4, ensure_ascii=False)

        print(f"Successfully created links for {len(all_channels_data)} channels!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    update_all_channels()
