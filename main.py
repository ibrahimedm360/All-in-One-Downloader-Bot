import telebot
import yt_dlp
import os

TOKEN = "8976242590:AAEshtx-vXSCvkZo95l_z4pb5axE2Hb0qtI"
bot = telebot.TeleBot(TOKEN)

# ইনকামের জন্য Force Join চ্যানেল
FORCE_CHANNEL = "@TomarChannelUsername" # তোমার চ্যানেল @ সহ

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "👋 লিংক পাঠাও!\nYouTube / TikTok / FB / Insta সব সাপোর্ট করে।\n\nExample: https://www.tiktok.com/...")

@bot.message_handler(func=lambda m: True)
def download(m):
    url = m.text.strip()
    if not url.startswith("http"):
        bot.send_message(m.chat.id, "সঠিক লিংক পাঠাও ভাই!")
        return

    msg = bot.send_message(m.chat.id, "⏳ ডাউনলোড হচ্ছে... ১০-২০ সেকেন্ড লাগবে")

    try:
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': 'video.%(ext)s',
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        
        # ভিডিও পাঠানো
        with open("video.mp4", "rb") as video:
            bot.send_video(m.chat.id, video, caption=f"✅ Done by @{bot.get_me().username}\n👉 আরো লাগলে {FORCE_CHANNEL} জয়েন করো")

        os.remove("video.mp4")
        bot.delete_message(m.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Error: লিংকটি প্রাইভেট বা সাপোর্ট করে না।\n{e}", m.chat.id, msg.message_id)

bot.infinity_polling()
