import re
import asyncio
from telethon import TelegramClient
from playwright.async_api import async_playwright
from twocaptcha import TwoCaptcha

# ==== CONFIG ====
API_ID = '26972239'
API_HASH = 'fa03ac53e4eacbf1c845e55bf7de09df'
TELEGRAM_CHANNEL = '@getstudyfevers'
MAX_MESSAGES = 30
UDEMY_SESSION_FILE = "udemy_auth.json"
CAPTCHA_API_KEY = '719d178459817c848886e9f0dfde8f63'  # 🔐 Replace with your actual API key

# ==== CAPTCHA SOLVER ====
solver = TwoCaptcha(CAPTCHA_API_KEY)

async def solve_captcha(page):
    print("🤖 CAPTCHA detected. Attempting to solve...")

    try:
        await page.locator("img").screenshot(path="captcha.png")
        result = solver.normal("captcha.png")
        print(f"✅ CAPTCHA Solved: {result['code']}")

        await page.locator("input[type='text']").fill(result['code'])
        await page.locator("button[type='submit']").click()
        await page.wait_for_timeout(3000)

    except Exception as e:
        print(f"❌ CAPTCHA solving failed: {e}")

# ==== LINK EXTRACTOR ====

def extract_coursefolder_link(message_text):
    lines = message_text.splitlines()
    for i, line in enumerate(lines):
        if "Enroll Now:" in line:
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith("https://coursefolder.net/") and "live-free-udemy-coupon.php" not in next_line:
                    return next_line
    return None

# ==== ENROLLMENT FUNCTION ====

async def enroll_in_course(url, context):
    page = await context.new_page()
    try:
        print(f"\n🌐 Visiting: {url}")
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(3000)

        # 🔍 CAPTCHA Check
        content = await page.content()
        if "captcha" in content.lower():
            await solve_captcha(page)

        # Click 'Get Free Coupon'
        try:
            await page.locator("text=Get Free Coupon").first.click(timeout=10000)
            print("🔗 Clicked 'Get Free Coupon'")
        except Exception:
            print("⚠️ 'Get Free Coupon' button not found.")
            await page.close()
            return

        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(5000)

        # Updated button list (prioritized)
        button_labels = ["Enroll now", "Enroll", "Start course", "Go to course", "Add to cart"]
        found = False

        for label in button_labels:
            try:
                buttons = page.locator(f"button:has-text('{label}')")
                count = await buttons.count()
                for i in range(count):
                    btn = buttons.nth(i)
                    if await btn.is_visible() and await btn.is_enabled():
                        print(f"👉 Clicking '{label}' button")
                        await btn.click(timeout=5000)
                        found = True
                        break
                if found:
                    break
            except Exception as e:
                print(f"⚠️ Issue with button '{label}': {e}")

        if not found:
            print(f"❌ No suitable 'Enroll' button found for: {url}")

        await page.wait_for_timeout(3000)

    except Exception as e:
        print(f"❗ Error processing course: {e}")
    finally:
        await page.close()

# ==== MAIN ====

async def main():
    print("📥 Connecting to Telegram...")
    client = TelegramClient('session', API_ID, API_HASH)
    await client.start()
    urls = []

    async for message in client.iter_messages(TELEGRAM_CHANNEL, limit=MAX_MESSAGES):
        if message.text:
            print("📩 Telegram Message:\n", message.text[:200])
            course_url = extract_coursefolder_link(message.text)
            if course_url:
                print(f"✅ Found course URL: {course_url}")
                urls.append(course_url)

    print(f"\n🔗 Found {len(urls)} valid course URLs to enroll.")

    if not urls:
        print("🚫 No valid links found.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(storage_state=UDEMY_SESSION_FILE)

        for url in urls:
            await enroll_in_course(url, context)

        await browser.close()

    print("🏁 All done!")

if __name__ == "__main__":
    asyncio.run(main())
