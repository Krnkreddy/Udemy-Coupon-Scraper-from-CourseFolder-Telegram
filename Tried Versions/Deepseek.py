import re
import time
import threading
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from telethon import TelegramClient, events
from webdriver_manager.chrome import ChromeDriverManager

# ===== CONFIGURATION =====
API_ID = '26972239'
API_HASH = 'fa03ac53e4eacbf1c845e55bf7de09df'
CHANNEL_ID = '@getstudyfevers'

# Chrome configuration
CHROME_PATH = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
PROFILE_PATH = os.path.join(os.getcwd(), "chrome_profile")
# =========================

# Global list for links
link_queue = []

def extract_coursefolder_link(message_text):
    """Improved link extraction from message text"""
    if not message_text:
        return None
        
    # Look for "Enroll Now:" pattern
    lines = message_text.splitlines()
    for i, line in enumerate(lines):
        if "Enroll Now:" in line and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line.startswith("https://") and "coursefolder.net" in next_line:
                return next_line
    
    # Fallback to URL search
    urls = re.findall(r'https?://[^\s\)]+', message_text)
    for url in urls:
        if 'coursefolder.net' in url and "live-free-udemy-coupon.php" not in url:
            return url
    
    return None

def telegram_listener():
    """Listen to Telegram channel and enqueue Udemy links"""
    print("Setting up Telegram client...")
    client = TelegramClient('session', API_ID, API_HASH)
    client.start()
    print("Telegram client authenticated successfully!")

    @client.on(events.NewMessage(chats=CHANNEL_ID))
    async def handler(event):
        if event.message.text:
            print("New message received")
            url = extract_coursefolder_link(event.message.text)
            if url:
                link_queue.append(url)
                print(f"Enqueued URL: {url}")

    print("Telegram listener running...")
    return client

def setup_driver():
    """Configure Chrome WebDriver with persistent profile"""
    os.makedirs(PROFILE_PATH, exist_ok=True)
    
    options = webdriver.ChromeOptions()
    options.binary_location = CHROME_PATH
    options.add_argument(f"--user-data-dir={PROFILE_PATH}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Check login status
    driver.get("https://www.udemy.com/")
    time.sleep(3)
    
    if "login" not in driver.current_url:
        print("Already logged in to Udemy")
        return driver
    
    # Manual login required
    driver.get("https://www.udemy.com/join/login-popup/")
    
    print("="*60)
    print("MANUAL LOGIN REQUIRED")
    print("1. Please login with Google in the Chrome window")
    print("2. Complete any 2FA if required")
    print("3. After successful login, return here and press Enter")
    print("="*60)
    
    input("Press Enter after you've logged in to Udemy...")
    
    # Verify login
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "img.udemy-avatar"))
        )
        print("Udemy login confirmed!")
    except TimeoutException:
        print("Warning: Login verification failed. Proceeding anyway...")
    
    return driver

def process_link(driver, url):
    """Redeem a free course from a coupon link"""
    print(f"\nProcessing: {url}")
    
    try:
        # Save current window handle
        main_window = driver.current_window_handle
        
        # Open link in new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(url)
        print(f"Opened URL: {driver.current_url}")

        # Step 1: Click "Get Free Coupon" or similar button
        try:
            # More flexible button detection
            coupon_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//*[" +
                    "contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'free coupon') or " +
                    "contains(., 'enroll for free') or " +
                    "contains(., 'enroll now') or " +
                    "contains(., 'get coupon') or " +
                    "contains(., 'get deal') or " +
                    "contains(., 'claim coupon') or " +
                    "contains(., 'redeem offer') or " +
                    "contains(., 'click to enroll') or " +
                    "contains(., 'go to offer')" +
                    "]"
                ))
            )
            coupon_btn.click()
            print("Clicked coupon button")
            time.sleep(3)  # Give more time for redirect
        except TimeoutException:
            print("No coupon button found - proceeding directly")

        # Step 2: Handle Udemy "Enroll Now"
        try:
            enroll_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[" +
                    "contains(., 'Enroll now') or " +
                    "contains(., 'Enroll for Free') or " +
                    "contains(., 'Add to cart') or " +
                    "contains(., 'Start Course') or " +
                    "contains(., 'Complete Enrollment')" +
                    "]"
                ))
            )
            enroll_btn.click()
            print("Clicked enroll button")
        except TimeoutException:
            print("Enroll button not found - checking if already enrolled")
            if "already enrolled" in driver.page_source.lower() or "already purchased" in driver.page_source.lower():
                print("Already enrolled in this course")
                return
            else:
                # Take a screenshot for debugging
                driver.save_screenshot("error_screenshot.png")
                print("Screenshot saved as error_screenshot.png")
                print("Page source saved to page_source.html")
                with open("page_source.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                raise

        # Step 3: Confirm enrollment
        try:
            confirm_btn = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//button[" +
                    "contains(., 'Complete Purchase') or " +
                    "contains(., 'Enroll now') or " +
                    "contains(., 'Place Order') or " +
                    "contains(., 'Confirm Enrollment') or " +
                    "contains(., 'Complete Checkout')" +
                    "]"
                ))
            )
            confirm_btn.click()
            print("Completed enrollment")
        except TimeoutException:
            print("Checkout page not required - course enrolled directly")

    except Exception as e:
        print(f"Error processing course: {str(e)}")
    finally:
        time.sleep(3)
        
        # Close all tabs except the main one
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                driver.close()
        
        driver.switch_to.window(main_window)
        print("Tabs closed, ready for next course")

def browser_automation():
    """Handle browser automation"""
    print("Setting up browser...")
    driver = setup_driver()
    
    print("\nSystem ready! Waiting for course links from Telegram...")
    while True:
        if link_queue:
            url = link_queue.pop(0)
            process_link(driver, url)
        time.sleep(1)

def main():
    # Start Telegram listener in main thread
    client = telegram_listener()
    
    # Start browser automation in a background thread
    browser_thread = threading.Thread(target=browser_automation, daemon=True)
    browser_thread.start()
    
    # Keep the main thread running for Telegram
    print("Press Ctrl+C to stop the script")
    client.run_until_disconnected()

if __name__ == "__main__":
    main()
