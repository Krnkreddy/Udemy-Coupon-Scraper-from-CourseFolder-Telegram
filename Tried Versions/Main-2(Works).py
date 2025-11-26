import asyncio
import json
import os
import re
from telethon import TelegramClient

# =====================================================================
# TELEGRAM SETTINGS
# =====================================================================
api_id = 26972239  
api_hash = "fa03ac53e4eacbf1c845e55bf7de09df"
group_username = "@getstudyfevers"

# =====================================================================
# SEEN IDS FILE
# =====================================================================
SEEN_IDS_FILE = "udemy_seen_ids.json"


def load_seen_ids():
    if os.path.exists(SEEN_IDS_FILE):
        with open(SEEN_IDS_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_seen_ids(seen_ids):
    with open(SEEN_IDS_FILE, "w") as f:
        json.dump(list(seen_ids), f)


# =====================================================================
# EXTRACT ONLY THE UDEMY LINK AFTER “Enroll Now:”
# =====================================================================
def extract_enroll_now_url(text: str):
    pattern = r"Enroll Now:\s*(https?://[^\s]+)"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return match.group(1) if match else None


# =====================================================================
# TELEGRAM SCRAPER
# =====================================================================
async def fetch_udemy_links_from_telegram():
    print("📥 Connecting to Telegram...")

    client = TelegramClient("session_name", api_id, api_hash)
    await client.start()

    seen_ids = load_seen_ids()
    new_seen = set()
    udemy_links = []

    async for msg in client.iter_messages(group_username, limit=500):
        if msg.id in seen_ids:
            continue

        new_seen.add(msg.id)

        if not msg.message:
            continue

        udemy_url = extract_enroll_now_url(msg.message)

        if udemy_url:
            print(f"🎯 Extracted Udemy Link: {udemy_url}")
            udemy_links.append(udemy_url)

    # Save updated seen IDs
    save_seen_ids(seen_ids.union(new_seen))

    await client.disconnect()
    return udemy_links


# =====================================================================
# MAIN SCRIPT
# =====================================================================
async def main():
    print("🚀 Fetching Udemy links from Telegram...")

    udemy_links = await fetch_udemy_links_from_telegram()

    if not udemy_links:
        print("❌ No Udemy links found under 'Enroll Now:'")
        return

    # Remove duplicates
    udemy_links = list(set(udemy_links))

    print("\n✅ Final Udemy Links:")
    for link in udemy_links:
        print(link)

    # Save to file
    with open("udemy_links.txt", "w", encoding="utf-8") as f:
        for url in udemy_links:
            f.write(url + "\n")

    print("\n💾 Saved to udemy_links.txt")


# =====================================================================
# ENTRY POINT
# =====================================================================
if __name__ == "__main__":
    asyncio.run(main())
