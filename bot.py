from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
import re

TOKEN = "8639850909:AAEVJ1lnwd2qnrms09WTNuPeff3n6L4YHiU""

expenses = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Yozavering, o‘zim hisoblayman 😎")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    usd = re.findall(r'(\d+)\s*\$|\b(\d+)\s*usd', text)
    uzs = re.findall(r'\b\d{3,}\b', text)

    added = False

    for u in uzs:
        expenses.append(("uzs", int(u)))
        added = True

    for d in usd:
        num = d[0] if d[0] else d[1]
        if num:
            expenses.append(("usd", int(num)))
            added = True

    if added:
        await update.message.reply_text("✅ Qo‘shildi")
    else:
        await update.message.reply_text("❌ Raqam topilmadi")

async def hisob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_uzs = sum(x[1] for x in expenses if x[0] == "uzs")
    total_usd = sum(x[1] for x in expenses if x[0] == "usd")

    await update.message.reply_text(
        f"📊 UZS: {total_uzs}\n💵 USD: {total_usd}"
    )

async def tozalash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    expenses.clear()
    await update.message.reply_text("🗑 Tozalandi")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hisob", hisob))
app.add_handler(CommandHandler("tozalash", tozalash))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
