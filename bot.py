import logging

import telegram

from webdriver import WebDriver
from utils import process_input, retry_on_error
from constants import ITEM_NAMES
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, ConversationHandler, filters
from difflib import get_close_matches

potential_items = [""]

logging.basicConfig(
    format='%(asctime)s:%(name)s: %(levelname)s - %(message)s',
    level=logging.INFO
)
web = WebDriver()
CHOOSING = 1


async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_message("nya")


async def getitem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = process_input(update.effective_message.text)
    global potential_items
    potential_items = get_close_matches(request, ITEM_NAMES, 5, 0.4)
    if not potential_items:
        await update.effective_message.reply_text("i couldn't find that item 💔")

    else:
        await update.message.reply_text("please choose one of the options",
                                        reply_markup=telegram.ReplyKeyboardMarkup([potential_items],
                                        resize_keyboard=True, one_time_keyboard=True))
    return CHOOSING


async def senditem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = update.message.text
    try:
        await retry_on_error(update.message.reply_photo(photo=open(f"pics/{item}.png", "rb"),
                                                        reply_markup=telegram.ReplyKeyboardRemove()))

    except FileNotFoundError:
        await update.message.reply_text(
            "whoops i couldn't find that on my local database this make take a minutee please be patient")
        web.fetch_item(item)
        await retry_on_error(update.message.reply_photo(photo=open(f"pics/{item}.png", "rb")))
    return ConversationHandler.END


async def endconv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ok bye")
    return ConversationHandler.END


if __name__ == '__main__':
    TOKEN = "6126139946:AAGBD4Y1NRxXFQ2JnPEhROD9SNVsgmiDjic"
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)
    MessageHandler(filters.TEXT, senditem)
    itemdesc_handler = ConversationHandler(entry_points=[CommandHandler("getitem", getitem)],
                                           states={
                                               CHOOSING: [
                                                   MessageHandler(filters.Text(potential_items) and (~filters.COMMAND),
                                                                  senditem)]},
                                           fallbacks=[CommandHandler("cancel", endconv)])

    application.add_handler(start_handler)
    application.add_handler(itemdesc_handler)

    application.run_polling()
