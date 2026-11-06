from flask import Flask
import threading
import os
import telebot
import yt_dlp

# Render কে বোঝানোর জন্য ছোট ওয়েবসাইট - এটা না থাকলে Deploy Failed হবে
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_flask).start()

# এখানে তোমার নতুন Token বসাবে
TOKEN = "8976242590:AAHTjeg7CacC9XzwP2lEsBGLF8AiBhyjxGg"
bot = telebot.TeleBot(TOKEN)

MY_CHANNEL = "@dhakacripto_downloader_bot"

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id,
        "👋 Dhaka Cripto Downloader এ স্বাগতম!\n\n"
        "শুধু লিংক পাঠাও, আমি ভিডিও ডাউনলোড করে দিবো।\n\n"
        "✅ YouTube\n"
        "✅ Facebook\n"
        "✅ TikTok\n"
        "✅ Instagram Reels"
    )

@bot.message_handler(func=lambda m: True)
def download(m):
    url = m.text.strip()
    if not url.startswith("http"):
        bot.send_message(m.chat.id, "❌ ভাই, সঠিক লিংক পাঠাও!")
        return

    msg = bot.send_message(m.chat.id, "⏳ ডাউনলোড হচ্ছে... ১৫-৩০ সেকেন্ড লাগবে...")

    try:
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")

        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': 'video.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Video')[:50]

        with open("video.mp4", "rb") as video:
            bot.send_video(m.chat.id, video, caption=f"✅ Done!\n🎬 {title}\n\n👉 আরো লাগলে {MY_CHANNEL} জয়েন করো")

        os.remove("video.mp4")
        bot.delete_message(m.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ ডাউনলোড হয়নি! লিংকটি প্রাইভেট হতে পারে।\nআরেকটা লিংক ট্রাই করো।", m.chat.id, msg.message_id)

print("Bot is Running...")
bot.infinity_polling()
