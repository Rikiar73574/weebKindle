from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
from Commands.commands import search, button_callback_handler
from Helpers.Subscription.subscription_manager import handle_all_messages

import Extensions.MangaDex.MangaDex

# Load the environment variables from .env file and ensure BOT_TOKEN is present
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if TOKEN is None:
    raise ValueError("Missing BOT_TOKEN environment variable")

# Initialize the application with the bot token and build it
app = ApplicationBuilder().token(TOKEN).build()

#COMMANDS
app.add_handler(CommandHandler("search", search))


#OTHER HANDLERS
app.add_handler(MessageHandler(filters.ALL, handle_all_messages), group=1)
app.add_handler(CallbackQueryHandler(button_callback_handler))

# POLLING
app.run_polling()


##TEST MANGADEX
#manga_results = MangaDex.search_manga('Naruto')
#if manga_results is not None:
#    for manga in manga_results:
#        print(manga)





