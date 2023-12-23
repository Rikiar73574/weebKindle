from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv
import os
from Commands.commands import search, button_callback_handler

# Load the environment variables from .env file and ensure BOT_TOKEN is present
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if TOKEN is None:
    raise ValueError("Missing BOT_TOKEN environment variable")

# Initialize the application with the bot token and build it
app = ApplicationBuilder().token(TOKEN).build()

# Add handlers for commands and callback queries
app.add_handler(CommandHandler("search", search))
app.add_handler(CallbackQueryHandler(button_callback_handler))

# Begin polling for updates
app.run_polling()








