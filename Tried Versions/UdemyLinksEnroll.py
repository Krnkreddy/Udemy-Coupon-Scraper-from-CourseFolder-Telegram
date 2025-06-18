import asyncio
from playwright.async_api import async_playwright

# ==== CONFIGURATION ====

# List of CourseFolder URLs that redirect to Udemy course pages
COURSE_URLS = [
    "https://coursefolder.net/personal-growth-affirmations-and-taking-action",
    "https://coursefolder.net/salesforce-administrator-certification-mock-exam-test",
    "https://coursefolder.net/professional-certificate-of-agile-and-scrum-business-analyst",
    "https://coursefolder.net/executive-diploma-in-strategic-management",
    "https://coursefolder.net/executive-diploma-in-engineering-management",
    # Add more course links here
]

# 📁 Path to Udemy session state (must be exported manually using browser with cookies extension)
UDEMY_LOGIN_STATE = "udemy_auth.json"

# ==== MAIN COURSE ENROLLMENT FUNCTION ====
async def enroll_in_course(url, context):
    page = await context.new_page()
    try:
        print(f"\n🌐 Visiting: {url}")
        await page.goto(url, timeout=60000)
        await page.wait_for_timeout(2000)

        # Step 1: Click on "Get Free Coupon"
        try:
            await page.locator("text=Get Free Coupon").first.click(timeout=5000)
            print("🔗 Clicked 'Get Free Coupon'")
        except:
            print("⚠️ 'Get Free Coupon' button not found.")
            return

        # Step 2: Wait for Udemy page to load
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(3000)

        # Step 3: (Optional) Debug - show buttons found
        buttons = await page.locator("button").all_inner_texts()
        print("🧪 Buttons found on Udemy page:", buttons)

        # Step 4: Click "Enroll now" (might require scrolling in some cases)
        try:
            enroll_button = page.locator('button[data-purpose="buy-this-course"]')
            await enroll_button.click(timeout=8000)
            print("✅ Clicked 'Enroll now'")
        except Exception as e:
            print(f"❌ Could not click 'Enroll now': {e}")

        await page.wait_for_timeout(2000)

    except Exception as e:
        print(f"❗ Error visiting course: {e}")
    finally:
        await page.close()

# ==== MAIN LOOP ====
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set headless=True to run without UI
        context = await browser.new_context(storage_state=UDEMY_LOGIN_STATE)

        for url in COURSE_URLS:
            await enroll_in_course(url, context)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
