import re
import asyncio
import os
from telethon import TelegramClient
from playwright.async_api import async_playwright
from twocaptcha import TwoCaptcha

# ==== CONFIG ====

# Load API credentials securely from environment variables
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")

# Telegram channel to monitor (set as an environment variable)
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL")  # # ⚠️ Replace with your target Telegram channel (e.g., '@yourchannel')

# Number of recent messages to check for course links
MAX_MESSAGES = 100

# Udemy login URL
UDEMY_LOGIN_URL = "https://www.udemy.com/join/login-popup/"

# CAPTCHA API Key (2Captcha) from environment variable
CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY")
solver = TwoCaptcha(CAPTCHA_API_KEY) if CAPTCHA_API_KEY else None

# ==== CAPTCHA SOLVER ====
async def solve_captcha(page):
    try:
        captcha_element = await page.query_selector("iframe[src*='captcha']")
        if captcha_element:
            print("🔍 CAPTCHA detected, attempting to solve...")
            site_key = await page.evaluate("() => document.querySelector('iframe[src*=\"captcha\"]').src")
            result = solver.recaptcha(sitekey=site_key, url=page.url)
            captcha_code = result['code']
            print("📸 CAPTCHA solved via 2Captcha.")
            await page.evaluate(f"document.getElementById('g-recaptcha-response').value = '{captcha_code}'")
            return True
        return False
    except Exception as e:
        print(f"❌ Error solving CAPTCHA: {e}")
        return False

# ==== LINK EXTRACTOR ====
def extract_course_url(message_text):
    pattern = r'https://coursefolder.net/[^\s]*(?!.*live-free-udemy-coupon\.php)'
    match = re.search(pattern, message_text)
    return match.group(0) if match else None

# ==== LOGIN FUNCTION ====
async def login_to_udemy(page):
    try:
        # Securely load Udemy credentials
        email = os.getenv("UDEMY_EMAIL")
        password = os.getenv("UDEMY_PASSWORD")

        if not email or not password:
            raise ValueError("❗ UDEMY_EMAIL or UDEMY_PASSWORD environment variable is not set.")

        print("🌐 Navigating to Udemy login page...")
        await page.goto(UDEMY_LOGIN_URL)
        await page.fill("input[name='email']", email)
        await page.fill("input[name='password']", password)
        await page.click("button[type='submit']")
        await page.wait_for_load_state("networkidle", timeout=30000)

        # Confirm successful login
        if await page.query_selector("a[href*='/user/']"):
            print("✅ Successfully logged into Udemy.")
            return True
        else:
            print("❌ Login failed: could not verify login.")
            return False
    except Exception as e:
        print(f"❌ Failed to login to Udemy: {e}")
        return False

# ==== ENROLLMENT FUNCTION ====
async def enroll_in_course(page, url):
    try:
        print(f"🌐 Navigating to course: {url}")
        await page.goto(url, timeout=30000)
        await page.wait_for_load_state("networkidle")

        coupon_button = await page.query_selector("a:has-text('Get Free Coupon')")
        if coupon_button:
            await coupon_button.click()
            print("🔗 Clicked 'Get Free Coupon' button")
            await page.wait_for_load_state("networkidle")
        else:
            print("⚠️ 'Get Free Coupon' button not found")
            return False

        if await solve_captcha(page):
            print("✅ CAPTCHA solved, continuing enrollment.")
        else:
            print("⚠️ No CAPTCHA detected or solving failed.")

        enroll_button = await page.query_selector("button:has-text('Enroll now')")
        if enroll_button:
            await enroll_button.click()
            print("🔗 Clicked 'Enroll now'")
            await page.wait_for_load_state("networkidle")
        else:
            print("⚠️ 'Enroll now' button not found")
            return False

        checkout_button = await page.query_selector("button:has-text('Enroll now')")
        if checkout_button:
            await checkout_button.click()
            print("✔️ Clicked 'Enroll now' on checkout page")
            await page.wait_for_load_state("networkidle")

            success_text = await page.query_selector("h1:has-text('Thanks for enrolling')")
            if success_text:
                print("✅ Successfully enrolled!")
                return True
            else:
                print("❌ Enrollment not confirmed")
                return False
        else:
            print("⚠️ No checkout page detected")
            return False
    except Exception as e:
        print(f"❌ Error enrolling in course {url}: {e}")
        return False

# ==== MAIN FUNCTION ====
async def main():
    if not API_ID or not API_HASH or not TELEGRAM_CHANNEL:
        print("❌ Missing TELEGRAM_API_ID, TELEGRAM_API_HASH, or TELEGRAM_CHANNEL environment variable.")
        return

    print("📥 Connecting to Telegram...")
    client = TelegramClient("session", API_ID, API_HASH)
    await client.start()

    try:
        urls = set()
        async for message in client.iter_messages(TELEGRAM_CHANNEL, limit=MAX_MESSAGES):
            if message.text:
                print(f"📩 Processing message: {message.text[:200]}...")
                course_url = extract_course_url(message.text)
                if course_url:
                    print(f"✅ Found course URL: {course_url}")
                    urls.add(course_url)

        print(f"\n🔗 Found {len(urls)} unique course URLs to enroll.")

        if not urls:
            print("🚫 No valid URLs found.")
            return

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            if await login_to_udemy(page):
                for url in urls:
                    success = await enroll_in_course(page, url)
                    print(f"{'🏆 Enrolled' if success else '🚫 Failed'}: {url}")
                    await asyncio.sleep(3)
            else:
                print("❌ Udemy login failed, aborting.")
                await browser.close()
                return

            await browser.close()
            print("🏁 All done!")

    except Exception as e:
        print(f"❌ Error in main: {e}")
    finally:
        await client.disconnect()

# ==== RUN SCRIPT ====
if __name__ == "__main__":
    asyncio.run(main())
