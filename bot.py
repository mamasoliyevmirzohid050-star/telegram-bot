from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
import re

TOKEN = "8639850909:AAEVJ1lnwd2qnrmso9WTNuPeff3n6L4YHiU"

expenses = []

ADMIN_ID = 311150720  # <-- BU YERGA O'ZINGIZNI ID QO'YING

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    dollars = re.findall(r'(\d+)\s*\$', text)
    numbers = re.findall(r'\d+', text)

    if not numbers:
        await update.message.reply_text("❌ Raqam topilmadi")
        return

    for d in dollars:
        expenses.append((float(d), "usd"))

    for n in numbers:
        if n not in dollars:
            expenses.append((float(n), "uzs"))

    await update.message.reply_text("✅ Qo‘shildi")

async def hisob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_uzs = sum(a for a, c in expenses if c == "uzs")
    total_usd = sum(a for a, c in expenses if c == "usd")

    await update.message.reply_text(
        f"📊 HISOB:\n\n"
        f"💰 {total_uzs:,.0f} so‘m\n"
        f"💵 ${total_usd:,.0f}"
    )

async def tozalash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Sizga ruxsat yo‘q")
        return

    global expenses
    expenses = []
    await update.message.reply_text("🗑 Hisob tozalandi")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("hisob", hisob))
app.add_handler(CommandHandler("tozalash", tozalash))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
