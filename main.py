#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import __version__ as TG_VER, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, \
    InlineKeyboardButton, InputMediaPhoto

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import requests
from bs4 import BeautifulSoup

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

KEYBOARD = [
        [
            KeyboardButton("Linkni yuboring", ),
        ],
    ]



# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    # print(update)
    # print(user)
    await update.message.reply_html(
        rf"Hi {user.first_name}! Please send me your searching item",
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    main_url = "https://asaxiy.uz/product"
    text = update.message.text
    url = main_url+"?key="+text
    # print(url)
    response = requests.get(f"{url}")
    soup = BeautifulSoup(response.content, 'html.parser')
    contents = soup.findAll('div', attrs={"class": "product__item"})[:10]

    if len(contents) == 0:
        await context.bot.send_message(
            chat_id=chat_id,
            text="Not found this item, sorry!"
        )

    # print(contents)
    for c in contents:
        title = c.find('h5', attrs={"class": "product__item__info-title"}).text
        image = c.find('img', attrs={"class": "img-fluid"}).get('data-src')
        price = c.find('span', attrs={"class": "product__item-price"}).text
        # print(title)
        if ".webp" in image:
            image = image[0:-5]
        # print(image)

        text = f"{title}\n\nNarxi: {price}"
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=image,
            caption=text,
        )


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5407487407:AAH0hYWGmvYb6rljo26rCq9SJoDoxqKAc3o").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()