import re
import asyncio
from telethon import TelegramClient
from playwright.async_api import async_playwright

# ==== CONFIG ====

# ⚠️ Replace these with your actual Telegram API credentials
API_ID = 'YOUR_API_ID'  # e.g., 123456
API_HASH = 'YOUR_API_HASH'  # e.g., 'abcd1234efgh5678ijkl90mn'

# ⚠️ Replace with your target Telegram channel (e.g., '@yourchannel')
TELEGRAM_CHANNEL = 'YOUR_TELEGRAM_CHANNEL'

# Number of recent messages to scan from the channel
MAX_MESSAGES = 30

# Path to saved Udemy session state
# 👉 Export cookies from your browser using an extension like:
#    "EditThisCookie" (Chrome) or "Cookie-Editor"
#    Save them as a JSON file named exactly as below
UDEMY_SESSION_FILE = "udemy_auth.json"

# ==== UTILS ====

def extract_coursefolder_link(message_text):
    """
    Extract only the coursefolder.net link directly following the 'Enroll Now:' line.
    """
    lines = message_text.splitlines()
    for i, line in enumerate(lines):
        if "Enroll Now:" in line:
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith("https://coursefolder.net/") and "live-free-udemy-coupon.php" not in next_line:
                    return next_line
    return None

async def enroll_in_course(url, context):
    """
    Automates the browser to enroll in a Udemy course using the shared coupon link.
    """
    page = await context.new_page()
    try:
        print(f"\n🌐 Visiting: {url}")
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(2000)

        try:
            await page.locator("text=Get Free Coupon").first.click(timeout=5000)
            print("🔗 Clicked 'Get Free Coupon'")
        except:
            print("⚠️ 'Get Free Coupon' not found.")
            await page.close()
            return

        await page.wait_for_load_state("networkidle")

        try:
            await page.locator("text=Enroll now").first.click(timeout=8000)
            await page.wait_for_timeout(1500)
            await page.locator("text=Enroll now").first.click(timeout=5000)
            print(f"✅ Enrolled in course: {url}")
        except:
            print("❌ 'Enroll now' not found or already enrolled.")

        await page.wait_for_timeout(2000)
    except Exception as e:
        print(f"❗ Error processing course: {e}")
    finally:
        await page.close()

# ==== MAIN ====

async def main():
    print("📥 Connecting to Telegram...")

    # Initialize Telegram client with API credentials
    client = TelegramClient('session', API_ID, API_HASH)
    await client.start()
    urls = []

    # Read recent messages from the channel and extract course links
    async for message in client.iter_messages(TELEGRAM_CHANNEL, limit=MAX_MESSAGES):
        if message.text:
            print("📩 Raw Message:\n", message.text)
            course_url = extract_coursefolder_link(message.text)
            if course_url:
                print(f"✅ Found course URL: {course_url}")
                urls.append(course_url)

    print(f"\n🔗 Found {len(urls)} valid course URLs to enroll.")

    if not urls:
        print("🚫 No valid links found.")
        return

    # Launch browser and load saved Udemy session for auto-login
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=UDEMY_SESSION_FILE)

        for url in urls:
            await enroll_in_course(url, context)

        await browser.close()

    print("🏁 All done!")

# Entry point
if __name__ == "__main__":
    asyncio.run(main())
