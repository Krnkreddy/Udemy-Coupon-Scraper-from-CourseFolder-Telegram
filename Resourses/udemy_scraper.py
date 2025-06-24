import asyncio
import json
import os
from playwright.async_api import async_playwright
from telethon import TelegramClient
from telethon.tl.types import MessageEntityUrl

# === TELEGRAM SETTINGS ===
# Replace the following placeholders with your own Telegram API credentials and target group/channel
api_id = YOUR_API_ID_HERE  # e.g., 123456
api_hash = 'YOUR_API_HASH_HERE'  # e.g., 'abc123xyz...'
group_username = '@your_target_group'  # e.g., '@examplegroup'

# === SEEN IDS FILE ===
# File used to store IDs of messages already processed, so we don't parse the same message again
SEEN_IDS_FILE = "udemy_seen_ids.json"

# Load previously seen Telegram message IDs from a file
def load_seen_ids():
    if os.path.exists(SEEN_IDS_FILE):
        with open(SEEN_IDS_FILE, 'r') as f:
            return set(json.load(f))
    return set()

# Save updated list of seen Telegram message IDs to file
def save_seen_ids(seen_ids):
    with open(SEEN_IDS_FILE, 'w') as f:
        json.dump(list(seen_ids), f)

# === UDEMY LINK EXTRACTOR ===
# This function uses Playwright to visit coursefolder.net links and extract the Udemy course URL
async def extract_udemy_links_from_coursefolder(playwright, coursefolder_links):
    browser = await playwright.chromium.launch(headless=True)  # Launch browser in headless mode
    context = await browser.new_context()
    page = await context.new_page()

    udemy_links = []

    for link in coursefolder_links:
        print(f"🌐 Visiting: {link}")
        try:
            await page.goto(link, timeout=0)  # Set timeout to 0 (wait indefinitely)

            # Skip links that redirect to CAPTCHA pages
            if "captcha" in page.url.lower():
                print(f"🤖 CAPTCHA detected. Skipping: {link}")
                continue

            # Wait for a link to a Udemy course
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
# This function connects to Telegram and retrieves coursefolder.net links from messages
async def get_coursefolder_links_from_telegram():
    print("📥 Connecting to Telegram...")

    # Create a new Telegram client session (the session will be saved as 'session_name.session')
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()

    seen_ids = load_seen_ids()
    new_seen_ids = set()
    course_links = []

    # Fetch the last 200 messages from the specified group or channel
    async for msg in client.iter_messages(group_username, limit=200):
        if msg.id in seen_ids:
            continue  # Skip messages we've already processed

        new_seen_ids.add(msg.id)

        # Check message for URLs
        if msg.entities:
            for entity in msg.entities:
                if isinstance(entity, MessageEntityUrl):
                    url = msg.message[entity.offset:entity.offset + entity.length]
                    if "coursefolder.net" in url:
                        print(f"✅ Found course URL: {url}")
                        course_links.append(url)

    await client.disconnect()

    # Save all seen message IDs (old + new)
    save_seen_ids(seen_ids.union(new_seen_ids))
    return course_links

# === MAIN FUNCTION ===
# Entry point that orchestrates Telegram scraping and Udemy link extraction
async def main():
    coursefolder_links = await get_coursefolder_links_from_telegram()

    if not coursefolder_links:
        print("🚫 No new course links found.")
        return

    # Use Playwright to extract Udemy links from the coursefolder pages
    async with async_playwright() as playwright:
        udemy_links = await extract_udemy_links_from_coursefolder(playwright, coursefolder_links)

        print("\n🎯 Final Udemy Course Links:")
        for url in udemy_links:
            print(url)

        # Save extracted Udemy links to a text file
        with open("udemy_links.txt", "w", encoding="utf-8") as f:
            for url in udemy_links:
                f.write(url + "\n")

# === ENTRY POINT ===
# Only run main() if this script is executed directly
if __name__ == "__main__":
    asyncio.run(main())
