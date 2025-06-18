import asyncio
from playwright.async_api import async_playwright
from telethon import TelegramClient
from telethon.tl.types import MessageEntityUrl

# === TELEGRAM SETTINGS ===
api_id = YOUR_API_ID  # Replace with your Telegram API ID (as an integer)
api_hash = 'YOUR_API_HASH'  # Replace with your Telegram API Hash (as a string)
group_username = '@your_telegram_group_or_channel'  # Replace with your Telegram group or channel username

# Extract Udemy coupon links from each coursefolder.net page
async def extract_udemy_links_from_coursefolder(playwright, coursefolder_links):
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()

    udemy_links = []

    for link in coursefolder_links:
        print(f"🌐 Visiting: {link}")
        try:
            # Navigate without timeout to handle slow networks
            await page.goto(link)

            # Skip page if CAPTCHA is detected
            if "captcha" in page.url.lower():
                print(f"🤖 CAPTCHA detected. Skipping: {link}")
                continue

            # Wait up to 30 seconds for Udemy coupon link
            await page.wait_for_selector("a[href^='https://www.udemy.com/course/']", timeout=30000)
            anchor = await page.query_selector("a[href^='https://www.udemy.com/course/']")
            udemy_url = await anchor.get_attribute('href')

            if udemy_url:
                print(f"✅ Udemy URL found: {udemy_url}")
                udemy_links.append(udemy_url)

        except Exception as e:
            print(f"❗ Error: {e}")

    await browser.close()
    return udemy_links

# Extract coursefolder.net links from the latest messages in a Telegram group or channel
async def get_coursefolder_links_from_telegram():
    print("📥 Connecting to Telegram...")
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start()

    course_links = []

    async for msg in client.iter_messages(group_username, limit=100):
        if msg.entities:
            for entity in msg.entities:
                if isinstance(entity, MessageEntityUrl):
                    url = msg.message[entity.offset:entity.offset + entity.length]
                    if "coursefolder.net" in url:
                        print(f"✅ Found course URL: {url}")
                        course_links.append(url)

    await client.disconnect()
    return course_links

# Main script logic
async def main():
    # Step 1: Get coursefolder.net links from Telegram messages
    coursefolder_links = await get_coursefolder_links_from_telegram()

    # Step 2: Extract Udemy links using Playwright
    async with async_playwright() as playwright:
        udemy_links = await extract_udemy_links_from_coursefolder(playwright, coursefolder_links)

        print("\n🎯 Final Udemy Course Links:")
        for url in udemy_links:
            print(url)

        # Optional: Save Udemy links to a file
        with open("udemy_links.txt", "w", encoding="utf-8") as f:
            for url in udemy_links:
                f.write(url + "\n")

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
