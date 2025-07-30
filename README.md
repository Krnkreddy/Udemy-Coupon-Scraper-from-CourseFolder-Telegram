# 🎓 Udemy Coupon Extractor from Telegram & CourseFolder

A Python automation tool that extracts free Udemy course links with active coupons from a Telegram channel or group that shares coursefolder.net links. It bypasses unnecessary waits, skips CAPTCHAs, and prints out clean Udemy URLs.

---

## 🚀 Features

- ✅ Fetches the latest 200 messages from a public Telegram channel
- ✅ Prioritizes unseen messages using a local history file
- ✅ Extracts CourseFolder.net links from messages
- ✅ Navigates each CourseFolder.net page using Playwright
- ✅ Detects and skips CAPTCHA pages
- ✅ Extracts final Udemy coupon URLs
- ✅ Outputs links to udemy_links.txt

---

## 📌 Use Case

You're subscribed to Telegram channels sharing free Udemy coupons using coursefolder.net URLs. Manually opening each link is time-consuming. This script automates the process and returns direct Udemy coupon links for easy enrollment.

---

## 🛠️ Tech Stack

- Python 3.10+
- Telethon
- Playwright
- asyncio
- Optional: BeautifulSoup (for enhanced HTML parsing, not used by default)

---

## ⚙️ Setup Instructions

1. Clone the repo:

```bash
git clone https://github.com/Krnkreddy/Udemy-Coupon-Scraper-from-CourseFolder-Telegram.git
cd Udemy-Coupon-Scraper-from-CourseFolder-Telegram
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
group_username = "@YourChannelOrGroupUsername"
```
To get Telegram API credentials:

Visit https://my.telegram.org/auth and create a new app.

4. Run the script:

```bash
python udemy_scraper.py
```

---

## ✅ Example Output

```bash
📥 Connecting to Telegram...
✅ Found course URL: https://coursefolder.net/python-for-ai
🌐 Visiting: https://coursefolder.net/python-for-ai
✅ Udemy URL found: https://www.udemy.com/course/python-for-ai/?couponCode=FREE2025
```

Use these links to enroll manually. They are also saved in udemy\_links.txt.

---

## ❗ Notes

* The script does not attempt to solve CAPTCHAs — it skips them automatically.
* Udemy links are printed in the terminal and saved to a local file.
* Make sure your Telegram account is authorized to access the group/channel.
* Only unseen messages are processed on each run, tracked via udemy\_seen\_ids.json.

---

## 🕐 Previous Tried Versions & Notes

We experimented with multiple methods before arriving at the final solution:

| Version                             | Description                                                                                  |
| ----------------------------------- | -------------------------------------------------------------------------------------------- |
| version1\_telegram\_only.py         | Fetched coursefolder.net links from Telegram, but lacked browser automation.                 |
| version2\_browser\_open.py          | Used Playwright to open pages, but tabs were closing early and caused timeouts.              |
| version3\_playwright\_open\_tabs.py | Tried to solve captchas and open tabs manually; hit timeout issues and inconsistent results. |

The final version resolves all these problems by:

* Removing strict timeouts
* Handling CAPTCHA detection cleanly
* Scraping only clean Udemy coupon URLs
* Storing seen Telegram message IDs for efficient repeated runs

---

## Help

Contributions are what makes the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "links or udemy".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/something...`)
3. Commit your Changes (`git commit -m 'Add some something...'`)
4. Push to the Branch (`git push origin feature/something...`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 💡 Credits

Developed using:

Telethon (https://github.com/LonamiWebs/Telethon)

Playwright Python (https://playwright.dev/python/)

For educational and personal use only. Not affiliated with Udemy or CourseFolder.


Developed by [Krnk Reddy](https://github.com/Krnkreddy) — feel free to fork, contribute, or share feedback!
