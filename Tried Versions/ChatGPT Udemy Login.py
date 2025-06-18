import asyncio
from playwright.async_api import async_playwright

async def save_udemy_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=50)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.udemy.com/join/login-popup/")

        print("🔓 Please log in manually and solve CAPTCHA.")
        print("⏳ Waiting 90 seconds for manual login...")
        await page.wait_for_timeout(90000)  # Give yourself 90s to log in

        await context.storage_state(path="udemy_auth.json")
        print("✅ Login session saved to udemy_auth.json")
        await browser.close()

asyncio.run(save_udemy_login())
