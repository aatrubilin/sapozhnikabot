import logging
import os
import time

import rhymer
import utils
from telegram import Bot, Update
from telegram.ext import CallbackContext, Filters, MessageHandler, Updater

BOT_TOKEN = os.environ["BOT_TOKEN"]
TIMEOUT_SEC = int(os.environ.get("TIMEOUT_SEC", 7200))
SWEARS_DATASET_PATH = os.environ.get("SWEARS_DATASET_PATH", "")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=LOG_LEVEL
)

swears_dataset = utils.get_dataset(SWEARS_DATASET_PATH)


def get_random_swear(*args, **kwargs):
    return utils.get_random_choice(swears_dataset)


REPLY_METHODS = [get_random_swear, rhymer.get_rhyme]


def should_reply(update: Update, context: CallbackContext):
    bot = context.bot
    if getattr(bot, "message_info", None) is None:
        logging.debug("Bot has not attr `message_info` -> True")
        bot.message_info = {}
        return True

    if not utils.random_bool():
        logging.debug("%s: random exit -> False", update.update_id)
        return False

    chat_id = update.message.chat.id
    if chat_id not in bot.message_info:
        logging.debug("%s: chat_id not in message_info -> True", update.update_id)
        return True

    ts_now = time.time()
    if ts_now - bot.message_info[chat_id]["ts"] < TIMEOUT_SEC:
        logging.debug("%s: timeout exit -> False", update.update_id)
        return False

    if bot.message_info[chat_id]["user_id"] == update.message.from_user.id:
        logging.debug("%s: duplicate user exit -> False", update.update_id)
        return False

    # Clear old keys
    for key in bot.message_info.keys():
        if ts_now - bot.message_info[key]["ts"] > 60 * 60 * 24 * 7:
            del bot.message_info[key]
    return True


def reply(update: Update, context: CallbackContext) -> None:
    """Reply the user message."""
    txt = update.message.text
    if not txt:
        return
    force_run = False
    if txt.startswith("@sapozhnikabot "):
        txt = txt.replace("@sapozhnikabot ", "")
        force_run = True

    if force_run or should_reply(update, context):
        reply_method = utils.get_random_choice(REPLY_METHODS)
        logging.debug("Reply method: %s", reply_method)
        reply = reply_method(txt)
        if reply:
            update.message.reply_text(reply)
            context.bot.message_info[update.message.chat.id] = {
                "ts": time.time(),
                "user_id": update.message.from_user.id,
            }
        else:
            logging.debug("Reply message is empty")


if __name__ == "__main__":
    bot = Bot(token=BOT_TOKEN)
    bot_info = bot.get_me()

    logging.info("Inited bot %s @%s", bot.first_name, bot.username)

    # Create the Updater and pass it your bot's token.
    updater = Updater(bot=bot)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Reply the message on Telegram only for groups
    dispatcher.add_handler(MessageHandler(Filters.chat_type.groups, reply))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
