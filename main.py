from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler, ContextTypes, filters
import requests
import logging
import re  # Untuk regex memeriksa URL
import os

BOT_TOKEN = os.getenv("BOT_KEY")

from keep_alive import keep_alive

TOKEN = BOT_TOKEN  # Ganti dengan token asli kamu

# Konfigurasi logging untuk debugging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


# Fungsi untuk menangani semua pesan masuk
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Debugging log
    logger.info(f"Pesan diterima: {text}")

    # Memeriksa apakah pesan mengandung URL TikTok
    if "tiktok.com" in text:
        # Jika URL TikTok ditemukan, balas dengan URL TikTok random
        await update.message.reply_text("Sedang memproses video...")

        try:
            # API untuk mengunduh video TikTok tanpa watermark
            api = f"https://tikwm.com/api/?url={text}"
            res = requests.get(api).json()

            # Memeriksa apakah video berhasil ditemukan
            if res.get("data") and res["data"].get("play"):
                video = res["data"]["play"]
                await update.message.reply_video(
                    video=video, caption="Berikut videonya tanpa watermark.")
            else:
                await update.message.reply_text("Gagal mengambil video.")
        except Exception as e:
            await update.message.reply_text(
                "Terjadi kesalahan saat mengunduh video.")
    elif text == "/start":
        await show_menu(update, context)
    else:
        await update.message.reply_text("Silakan pilih salah satu menu.")


# Fungsi untuk menangani perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_menu(update, context)


# Fungsi untuk menampilkan menu dengan tombol
# async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [[
#         InlineKeyboardButton("🎲 Random URL TikTok", callback_data="random")
#     ], [InlineKeyboardButton("⚙️ Setting", callback_data="setting")],
#                 [InlineKeyboardButton("❓ Help", callback_data="help")]]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     # Debugging log
#     logger.info("Menampilkan menu...")

#     if update.message:
#         await update.message.reply_text("Pilih menu:",
#                                         reply_markup=reply_markup)
#     else:
#         await update.callback_query.message.edit_text(
#             "Pilih menu:", reply_markup=reply_markup)


# Fungsi untuk menangani callback dari tombol
# async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # query = update.callback_query
    # data = query.data

    # Debugging log
    # logger.info(f"Callback diterima: {data}")

    # await query.answer()

    # if data == "random":
        # Menghasilkan URL TikTok random yang sesuai format
    #     random_tiktok_url = generate_random_tiktok_url()
    #     await query.edit_message_text(f"{random_tiktok_url}")
    # elif data == "setting":
        # Menampilkan info pengaturan bot
    #     await query.edit_message_text(
    #         "Pengaturan Bot: Bot ini digunakan untuk mendapatkan URL TikTok random dan memberikan bantuan."
    #     )
    # elif data == "help":
        # Menampilkan petunjuk penggunaan bot
    #     await query.edit_message_text(
    #         "Petunjuk:\n1. Klik 'Random URL TikTok' untuk mendapatkan URL TikTok acak.\n2. Klik 'Setting' untuk pengaturan bot.\n3. Klik 'Help' untuk bantuan."
    #     )
    # else:
    #     await query.edit_message_text("Menu tidak dikenal.")


# Fungsi untuk menghasilkan URL TikTok random yang sesuai format
# def generate_random_tiktok_url():
    # URL TikTok format yang diinginkan
    # random_id = random.randint(1000000000, 9999999999)
    # return f"https://vt.tiktok.com/Z{random_id}/"


# Menjalankan bot Telegram
app = ApplicationBuilder().token(TOKEN).build()

# Menambahkan handler untuk perintah /start, pesan URL TikTok, dan pesan lainnya
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
                               handle_message))

# Menambahkan handler untuk callback tombol
# app.add_handler(CallbackQueryHandler(handle_callback))

# Aktifkan server Flask agar Replit tetap hidup
keep_alive()

app.run_polling()
