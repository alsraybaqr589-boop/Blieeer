from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    filters,
)
import os

TOKEN = "8571330135:AAFZGOg1wDmw74g05bK1cZaYdsQYtjVyZpE"

GET_IP, GET_PORT = range(2)

servers = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📡 دز IP السيرفر")
    return GET_IP


async def get_ip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['ip'] = update.message.text

    await update.message.reply_text("🔌 هسه دز البورت")
    return GET_PORT


async def get_port(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['port'] = update.message.text

    user_id = update.effective_user.id

    servers[user_id] = {
        "ip": context.user_data['ip'],
        "port": context.user_data['port'],
        "status": "مطفي"
    }

    keyboard = [
        [InlineKeyboardButton("🟢 تشغيل البوت", callback_data="on")],
        [InlineKeyboardButton("🔴 اطفاء البوت", callback_data="off")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"✅ تم حفظ السيرفر\n\n"
        f"IP: {servers[user_id]['ip']}\n"
        f"PORT: {servers[user_id]['port']}\n"
        f"الحالة: {servers[user_id]['status']}",
        reply_markup=reply_markup,
    )

    return ConversationHandler.END


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in servers:
        await query.edit_message_text("❌ ماكو سيرفر محفوظ")
        return

    if query.data == "on":
        servers[user_id]['status'] = "شغال"

        await query.edit_message_text(
            f"🟢 البوت اشتغل\n\n"
            f"IP: {servers[user_id]['ip']}\n"
            f"PORT: {servers[user_id]['port']}"
        )

    elif query.data == "off":
        servers[user_id]['status'] = "مطفي"

        await query.edit_message_text("🔴 تم اطفاء البوت")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ تم الالغاء")
    return ConversationHandler.END


app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        GET_IP: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_ip)],
        GET_PORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_port)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv_handler)
app.add_handler(CallbackQueryHandler(buttons))

print("Bot Started...")
app.run_polling()
