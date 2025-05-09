from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests

from keep_alive import keep_alive

TOKEN = '8146022557:AAH-kvjv1ItB5AVYISvQGMhLO2wEqbPN6xg'  # Ganti dengan token asli kamu

# Fungsi untuk menangani semua pesan masuk
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "tiktok.com" in url:
        await update.message.reply_text("Sedang memproses video...")

        try:
            api = f"https://tikwm.com/api/?url={url}"
            res = requests.get(api).json()

            if res.get("data") and res["data"].get("play"):
                video = res["data"]["play"]
                await update.message.reply_video(video=video, caption="Berikut videonya tanpa watermark.")
            else:
                await update.message.reply_text("Gagal mengambil video.")
        except Exception as e:
            await update.message.reply_text("Terjadi kesalahan saat mengunduh video.")
    else:
        await update.message.reply_text("Silakan kirim link video TikTok.")

# Jalankan bot Telegram
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Aktifkan server Flask agar Replit tetap hidup
keep_alive()
app.run_polling()
