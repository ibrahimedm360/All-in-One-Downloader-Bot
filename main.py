from flask import Flask
import threading
import os
import telebot
import requests

# Render কে বোঝানোর জন্য - এটা না থাকলে Deploy Failed হবে
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()

# এখানে তোমার নতুন Token বসাবে
TOKEN = "8976242590:AAFtOdTp8GnYeavVIM3b1MkfJPhqNismnQo"
bot = telebot.TeleBot(TOKEN)

MY_CHANNEL = "@dhakacripto_downloader_bot"

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id,
        "👋 Dhaka Cripto Downloader এ স্বাগতম!\n\n"
        "শুধু লিংক পাঠাও, আমি ভিডিও ডাউনলোড করে দিবো।\n\n"
        "✅ YouTube\n"
        "✅ TikTok\n"
        "✅ Facebook\n"
        "✅ Instagram Reels\n\n"
        "লিংক পাঠাও, যেমন:\nhttps://www.tiktok.com/@user/video/..."
    )

@bot.message_handler(func=lambda m: True)
def download(m):
    # লিংকটা ছোট করে নেওয়া - ? এর পরের সব কেটে দেওয়া
    raw_url = m.text.strip()
    url = raw_url.split('?')[0].split('&')[0].split()[0]

    if not url.startswith("http"):
        bot.send_message(m.chat.id, "❌ ভাই, সঠিক লিংক পাঠাও!")
        return

    msg = bot.send_message(m.chat.id, "⏳ ডাউনলোড হচ্ছে... ১৫-৩০ সেকেন্ড লাগবে...")

    try:
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")

        # Cobalt API দিয়ে ডাউনলোড - yt-dlp এর বদলে
                # TikTok হলে TikWM দিয়ে, বাকিগুলো Cobalt দিয়ে
        if "tiktok.com" in url:
            r = requests.get(f"https://www.tikwm.com/api/?url={raw_url}", timeout=60)
            data = r.json()
            video_url = data.get("data", {}).get("play")
        else:
            r = requests.post("https://api.cobalt.tools/api/json",
                json={"url": raw_url, "downloadMode": "auto"},
                headers={"Accept": "application/json", "Content-Type": "application/json"},
                timeout=60
            )
            video_url = r.json().get("url")

        if not video_url:
            raise Exception("Cobalt fail")

        # ভিডিওটা নামিয়ে পাঠানো
        v = requests.get(video_url, timeout=90).content
        with open("video.mp4", "wb") as f:
            f.write(v)

        with open("video.mp4", "rb") as video:
            bot.send_video(m.chat.id, video, caption=f"✅ Done!\n\n👉 আরো ডাউনলোড করতে {MY_CHANNEL} জয়েন করো")

        os.remove("video.mp4")
        bot.delete_message(m.chat.id, msg.message_id)

    except Exception as e:
        try:
            bot.edit_message_text("❌ ডাউনলোড হয়নি! লিংকটি প্রাইভেট হতে পারে।\nআরেকটা ছোট লিংক ট্রাই করো।", m.chat.id, msg.message_id)
        except:
            pass

print("Bot is Running...")
bot.infinity_polling()
