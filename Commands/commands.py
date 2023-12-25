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

        
        subscription_data=f"Subscribe|{update.effective_chat.id}|{result['source']}|{result['title']}|{result['last_chapter']}"
        download_data=f"Download|{update.effective_chat.id}|{result['last_chapter']}"
        subscription_id = SubscriptionManager.save_subscription_data(subscription_data)
        download_id= SubscriptionManager.save_subscription_data(download_data)
        subscribe_button = InlineKeyboardButton(
            text="Subscribe",
            callback_data=subscription_id
        )
        download_button = InlineKeyboardButton(
            text="Download",
            callback_data=download_id
        )
        reply_markup = InlineKeyboardMarkup([[subscribe_button,download_button]])

        
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
        _, chat_id, source, title, last_chapter = callback_data.split("|")
    
        # Assuming subscribe_user method signature has been updated to include title,
        # or if it still accepts the full callback_data for processing.
        response = SubscriptionManager.add_title(chat_id, source, title, last_chapter)
    
        match response:
            case "subscribe:0":
                await context.bot.send_message(chat_id=chat_id, text="You have successfully subscribed!")
                filepath = (PDFDownloader(last_chapter)).download_pdf()
                # You may want to do something with the downloaded PDF here
    
            case "subscribe:1":
                await context.bot.send_message(chat_id=chat_id, text="Already subscribed.")
            
    if callback_data.startswith("Download|"):
        _, chat_id, last_chapter = callback_data.split("|")
        filepath = (PDFDownloader(last_chapter)).download_pdf()
        await context.bot.send_document(chat_id=chat_id, document=filepath)


