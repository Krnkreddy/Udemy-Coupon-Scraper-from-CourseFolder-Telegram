import webbrowser
import time
import os

def open_udemy_links():
    # Get the current directory where the script is running
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "udemy_links.txt")

    # Check if the file exists
    if not os.path.exists(file_path):
        print("❌ File 'udemy_links.txt' not found in the same directory.")
        return

    # Read all links from the file
    with open(file_path, "r") as file:
        links = [line.strip() for line in file if line.strip()]

    if not links:
        print("⚠️ No links found in 'udemy_links.txt'.")
        return

    print(f"✅ Found {len(links)} links. Opening in browser...")

    # Open each link in the default browser
    for i, link in enumerate(links, 1):
        print(f"🌐 Opening link {i}: {link}")
        webbrowser.open_new_tab(link)
        time.sleep(1)  # short delay between opening tabs (adjust if needed)

#   print("🎉 All links opened successfully! Browser will remain open.")
    print("🎉 All links opened successfully!")

if __name__ == "__main__":
    open_udemy_links()
