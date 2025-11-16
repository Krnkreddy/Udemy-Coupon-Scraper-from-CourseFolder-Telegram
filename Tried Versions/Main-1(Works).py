# Updated the noew code reduce the time of running like the extractinglike takes the time of 1-10 sec and gived the link from the coursefolder.net not the correct link

import asyncio
import json
import os
from playwright.async_api import async_playwright
from telethon import TelegramClient
from telethon.tl.types import MessageEntityUrl

# === TELEGRAM SETTINGS ===
api_id = 26972239  # Replace with your own Telegram API ID
api_hash = 'fa03ac53e4eacbf1c845e55bf7de09df'  # Replace with your own API hash
group_username = '@getstudyfevers'  # Replace with your target Telegram channel or group
# @Coursevania
# @getstudyfevers

# === SEEN IDS FILE ===
SEEN_IDS_FILE = "udemy_seen_ids.json"

# Load previously seen Telegram message IDs
def load_seen_ids():
    if os.path.exists(SEEN_IDS_FILE): 
        with open(SEEN_IDS_FILE, 'r') as f:
            return set(json.load(f))
    return set()

# Save updated seen message IDs
def save_seen_ids(seen_ids):
    with open(SEEN_IDS_FILE, 'w') as f:
        json.dump(list(seen_ids), f)

# === UDEMY LINK EXTRACTOR ===
async def extract_udemy_links_from_coursefolder(playwright, coursefolder_links):
    browser = await playwright.chromium.launch(headless=True)   
    context = await browser.new_context()
    page = await context.new_page()

    udemy_links = []

    for link in coursefolder_links:
        print(f"🌐 Visiting: {link}")
        try:
            await page.goto(link, timeout=0)  # No timeout in case of slow network

            if "captcha" in page.url.lower():
                print(f"🤖 CAPTCHA detected. Skipping: {link}")
                continue

            # Wait for Udemy link (if any) on the page
            await page.wait_for_selector("a[href^='https://www.udemy.com/course/']", timeout=10000)
            anchor = await page.query_selector("a[href^='https://www.udemy.com/course/']")
            udemy_url = await anchor.get_attribute('href')

            if udemy_url:
                print(f"✅ Udemy URL found: {udemy_url}")
                udemy_links.append(udemy_url)

        except Exception as e:
            print(f"❗ Error visiting {link}: {e}")

    await browser.close()
    return udemy_links

# === TELEGRAM PARSER ===
async def get_coursefolder_links_from_telegram():
    print("📥 Connecting to Telegram...")
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()

    seen_ids = load_seen_ids()
    new_seen_ids = set()
    course_links = []

    async for msg in client.iter_messages(group_username, limit=500):  # Fetch last 500 messages
        if msg.id in seen_ids:
            continue

        new_seen_ids.add(msg.id)

        if msg.entities:
            for entity in msg.entities:
                if isinstance(entity, MessageEntityUrl):
                    url = msg.message[entity.offset:entity.offset + entity.length]
                    if "coursefolder.net" in url:
                        print(f"✅ Found course URL: {url}")
                        course_links.append(url)

    await client.disconnect()
    save_seen_ids(seen_ids.union(new_seen_ids))
    return course_links

# === MAIN FUNCTION ===
async def main():
    coursefolder_links = await get_coursefolder_links_from_telegram()

    if not coursefolder_links:
        print("🚫 No new course links found.")
        return

    async with async_playwright() as playwright:
        udemy_links = await extract_udemy_links_from_coursefolder(playwright, coursefolder_links)

        print("\n🎯 Final Udemy Course Links:")
        for url in udemy_links:
            print(url)

        # Save to file
        with open("udemy_links.txt", "w", encoding="utf-8") as f:
            for url in udemy_links:
                f.write(url + "\n")

# === ENTRY POINT ===
if __name__ == "__main__":
    asyncio.run(main())
