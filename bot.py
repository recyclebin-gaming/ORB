import logging
from utils import fetch_item, process_input, poll_webdriver
from constants import ITEM_NAMES
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from difflib import get_close_matches


logging.basicConfig(
    format='%(asctime)s:%(name)s: %(levelname)s - %(message)s',
    level=logging.INFO
)
driver = poll_webdriver()


async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    await update.effective_chat.send_message("nya")


async def getitem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    request = process_input(update.effective_message.text)
    item_name = get_close_matches(request, ITEM_NAMES)[0]
    if not item_name:
        await update.effective_message.reply_text("i couldn't find that item 💔")

    else:
        message = await update.effective_message.reply_text("holdon im thinking")
        try:
            await update.effective_message.reply_photo(photo=open(f"pics/{item_name}.png", "rb"))
            await message.delete()
            return

        except FileNotFoundError:
            await message.edit_text("whoops we ran into some issues this might take a bit be patient please")
            fetch_item(request, driver)
            await update.effective_message.reply_photo(photo=open(f"pics/{item_name}.png", "rb"))
            await message.delete()
            return

    await update.effective_message.reply_text("uh oh something went wrong try again please")

if __name__ == '__main__':
    TOKEN = "6126139946:AAGBD4Y1NRxXFQ2JnPEhROD9SNVsgmiDjic"
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)
    getitem_handler = CommandHandler("getitem", getitem)

    application.add_handler(start_handler)
    application.add_handler(getitem_handler)

    application.run_polling()
