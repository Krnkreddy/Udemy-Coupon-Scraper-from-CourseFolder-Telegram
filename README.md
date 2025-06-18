# 🎓 Udemy Coupon Extractor from Telegram & CourseFolder

A Python automation tool that extracts free Udemy course links with active coupons from a Telegram channel or group that shares coursefolder.net links. It bypasses unnecessary waits, skips CAPTCHAs, and prints out clean Udemy URLs.

---

## 🚀 Features

- 📥 Fetches messages from a specified Telegram group or channel.
- 🔗 Extracts and visits all coursefolder.net links.
- 🔍 Automatically finds working Udemy coupon links.
- ⏩ Skips CAPTCHA-protected or broken links.
- 📋 Outputs clean Udemy coupon URLs — no enrollment or interaction required.

---

## 📌 Use Case

You're subscribed to Telegram channels sharing free Udemy coupons using coursefolder.net URLs. Manually opening each link is time-consuming. This script automates the process and returns direct Udemy coupon links for easy enrollment.

---

## 🛠️ Tech Stack

- Python 3.10+
- Telethon
- Playwright
- asyncio
- Optional: BeautifulSoup (for enhanced HTML parsing)

---

## ⚙️ Setup Instructions

1. Clone the repo:

```bash
git clone https://github.com/yourusername/udemy-coupon-extractor.git
cd udemy-coupon-extractor
````

2. Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

3. Configure Telegram API:

Edit the script (e.g., teleopenauto.py) and add your Telegram API credentials:

```python
api_id = 123456     # Replace with your API ID
api_hash = "your_api_hash"
group_username = "YourGroupOrChannelUsername"
```

4. Run the script:

```bash
python teleopenauto.py
```

---

## ✅ Example Output

```bash
✅ Udemy URL found: https://www.udemy.com/course/python-for-beginners/?couponCode=FREECODE2025
✅ Udemy URL found: https://www.udemy.com/course/html-css-js-projects/?couponCode=HTMLMASTER
✅ Udemy URL found: https://www.udemy.com/course/data-science-bootcamp/?couponCode=DATADEAL
```

Use these links to enroll manually.

---

## ❗ Notes

* The script does not attempt to solve CAPTCHAs — it skips them automatically.
* Udemy links are printed in the terminal and can be copied manually.
* Make sure your Telegram account is authorized to access the group/channel.

---

🕐 Previous Tried Versions & Notes
We experimented with multiple methods before arriving at the final solution:

| Version                             | Description                                                                                  |
| ----------------------------------- | -------------------------------------------------------------------------------------------- |
| version1\_telegram\_only.py         | Fetched coursefolder.net links from Telegram, but lacked browser automation.                 |
| version2\_browser\_open.py          | Used Playwright to open pages, but tabs were closing early and caused timeouts.              |
| version3\_playwright\_open\_tabs.py | Tried to solve captchas and open tabs manually; hit timeout issues and inconsistent results. |


Final version resolves all these problems by:
- Removing strict timeouts
- Handling CAPTCHA failures
- Scraping only clean Udemy coupon URLs

---

## 📝 License

This project is licensed under the MIT License.

---

## 💡 Credits

Developed by [Krnk Reddy]([https://github.com/yourusername](https://github.com/Krnkreddy)) — feel free to contribute or fork!
