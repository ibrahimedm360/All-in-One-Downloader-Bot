import os
import requests
import telebot
from flask import Flask

BOT_TOKEN = os.environ.get("8976242590:AAFtOdTp8GnYeavVIM3b1MkfJPhqNismnQo")
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Dhaka Cripto Downloader এ স্বাগতম\n\nশুধু লিংক পাঠাও, আমি ভিডিও ডাউনলোড করে দিবো।\n\n✅ YouTube\n✅ TikTok\n✅ Facebook\n✅ Instagram Reels\n\nলিংক পাঠাও, যেমন:\nhttps://www.tiktok.com/@user/video/...")

@bot.message_handler(func=lambda m: True)
def download(message):
    chat_id = message.chat.id
    raw_url = message.text.strip()

    if "http" not in raw_url:
        bot.send_message(chat_id, "❌ সঠিক লিংক পাঠাও।")
        return

    # ? এর পরের অংশ কেটে ফেলা
    url = raw_url.split("?")[0].split("&")[0]
    clean_url = raw_url.split("?")[0]

    bot.send_message(chat_id, "⏳ ডাউনলোড হচ্ছে, একটু ওয়েট করো...")

    # ---------- TikTok ----------
    if "tiktok.com" in url:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(f"https://api.tikwm.com/api/?url={clean_url}", headers=headers, timeout=25)
            j = r.json()
            d = j.get("data", {})
            video_url = d.get("play") or d.get("wmplay") or d.get("hdplay")
            if not video_url:
                bot.send_message(chat_id, "❌ TikWM ভিডিও পায়নি, অন্য লিংক দাও।")
                return
            bot.send_video(chat_id, video_url, caption="✅ TikTok ডাউনলোড ডান!")
            return
        except Exception as e:
            bot.send_message(chat_id, f"❌ Error: {e}")
            return

    # ---------- YouTube / Facebook / Instagram ----------
    try:
        r = requests.post("https://api.cobalt.tools/api/json", json={"url": clean_url}, headers={"Accept": "application/json", "Content-Type": "application/json"}, timeout=25)
        data = r.json()
        video_url = data.get("url")
        if not video_url:
            bot.send_message(chat_id, "❌ ডাউনলোড হয়নি! লিংকটি প্রাইভেট হতে পারে।\nআরেকটা ছোট লিংক ট্রাই করো।")
            return
        bot.send_video(chat_id, video_url, caption="✅ ডাউনলোড ডান!")
    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {e}")

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))).start()
    bot.infinity_polling()
