from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext, CallbackQueryHandler
import os
import json
from Extensions.LupiTeam.LupiTeam import LupiTeam
from Helpers.Subscription.subscription_manager import SubscriptionManager
from .Pdf.processing import PDFDownloader


def escape_markdown(text):
    escape_chars = '_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{c}' if c in escape_chars else c for c in text)

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("Please provide a query after the /search command.")
        return

    lt = LupiTeam()
    search_results = lt.SearchManga(query)

    
    formatted_results = []
    for result in search_results:
        title = escape_markdown(result['title'])
        url = escape_markdown(result['url'])
        author = escape_markdown(result['author'])
        status = escape_markdown(result['status'])
        last_chapter = escape_markdown(result['last_chapter'])
        thumbnail_url = result['thumbnail']  

        caption = (
            f"*Title:* [{title}]({url})\n"
            f"*Author:* {author}\n"
            f"*Status:* {status}\n"
            f"*Last Chapter:* [Read Here]({last_chapter})"
        )

        
        button_data=f"Subscribe|{update.effective_chat.id}|{update.effective_chat.effective_name}|{result['source']}|{result['title']}|{result['last_chapter']}"
        subscription_id = SubscriptionManager.save_subscription_data(button_data)
        subscribe_button = InlineKeyboardButton(
            text="Subscribe",
            callback_data=subscription_id
        )
        reply_markup = InlineKeyboardMarkup([[subscribe_button]])

        
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=thumbnail_url,
            caption=caption,
            parse_mode='MarkdownV2',
            reply_markup=reply_markup
        )


async def button_callback_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    callback_data = SubscriptionManager.load_subscription_data(query.data)

    if callback_data.startswith("Subscribe|"):
        _,chat_id, username, source, title, last_chapter = callback_data.split("|")
        response = SubscriptionManager.subscribe_user(callback_data)
        match response:
            case "subscribe:0":
                await context.bot.send_message(chat_id=chat_id, text="You have successfully subscribed!")
                filepath=(PDFDownloader(last_chapter)).download_pdf()

            case "subscribe:1":
                await context.bot.send_message(chat_id=chat_id, text="Already subscribed.")

