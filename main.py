from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import requests
import random

from keep_alive import keep_alive

TOKEN = '8146022557:AAH-kvjv1ItB5AVYISvQGMhLO2wEqbPN6xg'  # Ganti dengan token asli kamu


# Fungsi untuk menangani semua pesan masuk
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Jika user mengetik /start atau pesan lainnya, tampilkan menu
    if text == "/start":
        await show_menu(update, context)
    else:
        await update.message.reply_text("Silakan pilih salah satu menu.")


# Fungsi untuk menampilkan menu dengan tombol
async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[
        InlineKeyboardButton("🎲 Random URL TikTok", callback_data="random")
    ], [InlineKeyboardButton("⚙️ Setting", callback_data="setting")],
                [InlineKeyboardButton("❓ Help", callback_data="help")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("Pilih menu:",
                                        reply_markup=reply_markup)
    else:
        await update.callback_query.message.edit_text(
            "Pilih menu:", reply_markup=reply_markup)


# Fungsi untuk menangani callback dari tombol
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    await query.answer()

    if data == "random":
        # Menghasilkan URL TikTok random
        random_tiktok_url = generate_random_tiktok_url()
        await query.edit_message_text(
            f"Berikut adalah URL TikTok random: {random_tiktok_url}")
    elif data == "setting":
        # Menampilkan info pengaturan bot
        await query.edit_message_text(
            "Pengaturan Bot: Bot ini digunakan untuk mendapatkan URL TikTok random dan memberikan bantuan."
        )
    elif data == "help":
        # Menampilkan petunjuk penggunaan bot
        await query.edit_message_text(
            "Petunjuk:\n1. Klik 'Random URL TikTok' untuk mendapatkan URL TikTok acak.\n2. Klik 'Setting' untuk pengaturan bot.\n3. Klik 'Help' untuk bantuan."
        )
    else:
        await query.edit_message_text("Menu tidak dikenal.")


# Fungsi untuk menghasilkan URL TikTok random
def generate_random_tiktok_url():
    # Misalnya, kita buat URL TikTok acak dengan ID video acak
    random_id = random.randint(1000000000, 9999999999)
    return f"https://www.tiktok.com/@user/video/{random_id}"


# Menjalankan bot Telegram
app = ApplicationBuilder().token(TOKEN).build()

# Menambahkan handler untuk pesan dan callback
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
                               handle_message))
app.add_handler(CallbackQueryHandler(handle_callback))

# Aktifkan server Flask agar Replit tetap hidup
keep_alive()

app.run_polling()
