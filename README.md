# 🎓 Udemy Coupon Extractor from Telegram

Extracts **direct Udemy coupon links** shared inside Telegram channels — clean, fast, and captcha-free.

This tool scans messages from a Telegram channel/group and extracts **only the Udemy link placed under “Enroll Now:”**, ignoring all other coursefolder links, random URLs, or irrelevant content.

---

## 🚀 Features

* 🔍 Extracts **direct Udemy coupon links** under
  `Enroll Now:`
* ⚡ Fast — no Playwright/captcha/browser needed
* 🧠 Tracks previously seen messages
* 📁 Saves links cleanly to `udemy_links.txt`
* 🛡 Avoids coursefolder redirects completely
* 🎯 Works with realistic Telegram message formats

---

## 📌 Perfect For

If you follow Telegram channels that post free Udemy coupons, this script helps you:

✔ Skip all ads, redirects & coursefolder pages
✔ Extract only the *final Udemy coupon link*
✔ Keep everything clean and automated

---

## 🛠 Tech Stack

* **Python 3.10+**
* **Telethon** (Telegram API client)
* **Regex** for smart Udemy link extraction
* **JSON** for storing processed message IDs

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Krnkreddy/Udemy-Coupon-Scraper-from-CourseFolder-Telegram.git
cd Udemy-Coupon-Scraper-from-CourseFolder-Telegram
```

### 2️⃣ Install dependencies

```bash
pip install telethon
```

### 3️⃣ Configure your Telegram API

Edit the script (e.g., `test.py`):

```python
api_id = 123456
api_hash = "your_api_hash"
group_username = "@YourTelegramChannel"
```

To get API credentials:
👉 [https://my.telegram.org/auth](https://my.telegram.org/auth)

### 4️⃣ Run the script

```bash
python test.py
```

---

## 🧠 How Link Extraction Works

Each Telegram message may contain many URLs, such as:

* coursefolder links
* language/category links
* random promo links

But you want **only the Udemy link**, located directly after:

```
Enroll Now:
https://www.udemy.com/course/.../?couponCode=XYZ
```

The script uses this smart regex:

```python
Enroll Now:\s*(https?://[^\s]+)
```

✔ Extracts correct Udemy URL
✔ Ignores extra links
✔ Works with line breaks
✔ Case-insensitive

---

## 📝 Example Output

```
📥 Connecting to Telegram...
🎯 Extracted Udemy Link: https://www.udemy.com/course/genai-revolution-transform-rd-with-cutting-edge-ai-tools/?couponCode=AUTUMN2025GO
```

Saved inside:

```
udemy_links.txt
```

---

## 📁 Project Structure

```
📦 UdemyTelegramExtractor
 ├── test.py                # Main script
 ├── udemy_seen_ids.json    # Tracks processed messages
 ├── udemy_links.txt        # Output file
 ├── README.md              # Documentation
```

---

## 🔄 Previous Version Notes (History)

| Version                   | Description                                                      |
| ------------------------- | ---------------------------------------------------------------- |
| v1 – Coursefolder Scraper | Used Playwright to open coursefolder pages; slow & captcha-prone |
| v2 – Browser Tabs Model   | Opened coursefolder in tabs; inconsistent results                |
| v3 – Hybrid Method        | Partial telegram + browser automation                            |
| **v4 – Final (Current)**  | Clean regex-only Udemy extraction. Fast. No CAPTCHAs. Accurate.  |

---

## 🤝 Contributing

Contributions make the open-source community amazing!
Pull requests, bug reports, or ideas are **always welcome**.

### Steps to contribute:

1. Fork the project
2. Create a feature branch

   ```bash
   git checkout -b feature/new-idea
   ```
3. Commit changes

   ```bash
   git commit -m "Add new feature"
   ```
4. Push to GitHub

   ```bash
   git push origin feature/new-idea
   ```
5. Open a Pull Request 🚀

---

## ⭐ Show Support

If this project helped you, **please give it a star on GitHub** — it means a lot!  
👉 [https://github.com/Krnkreddy/Udemy-Coupon-Scraper-from-CourseFolder-Telegram](https://github.com/Krnkreddy/Udemy-Coupon-Scraper-from-CourseFolder-Telegram)

---

## 📝 License

This project is under the **MIT License**.

---

## 💡 Credits

Built using:

* **Telethon** → Telegram Client
* **Python Regex** → Clean Udemy link parsing

Developed by **[Krnk Reddy](https://github.com/Krnkreddy)**
Feel free to fork, improve, and experiment!
