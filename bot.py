from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# 🔑 Replace these
TOKEN = "8023940447:AAE_Pgk-CcCk0e0OiqJJc4qRUaMU3BLDpzQ"
OWNER_ID = 7858266783   # paste your Telegram ID here

NAME = 0

# 🚀 Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎤 Welcome!\n\nEnter your name:")
    return NAME

# 📝 Save name
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text

    with open("users.txt", "a") as f:
        f.write(name + "\n")

    await update.message.reply_text("✅ Registered successfully!")
    return ConversationHandler.END

# 👑 Show users (ONLY YOU)
async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ You are not allowed.")
        return

    try:
        with open("users.txt", "r") as f:
            users = f.read()

        if users.strip() == "":
            await update.message.reply_text("No users yet.")
        else:
            await update.message.reply_text("📋 Users:\n\n" + users)

    except FileNotFoundError:
        await update.message.reply_text("No data found.")

# ❌ Cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

# ⚙️ Setup bot
app = ApplicationBuilder().token(TOKEN).build()

conv = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

app.add_handler(conv)
app.add_handler(CommandHandler("users", show_users))

# ▶️ Run bot
app.run_polling()

