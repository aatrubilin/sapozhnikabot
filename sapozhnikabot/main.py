import logging
import os

import rhymer
import utils
from db import Database
from telegram import Bot, Update
from telegram.ext import CallbackContext, ContextTypes, Filters, MessageHandler, Updater

BOT_TOKEN = os.environ["BOT_TOKEN"]
TIMEOUT_SEC = int(os.environ.get("TIMEOUT_SEC", 7200))
SWEARS_DATASET_PATH = os.environ.get("SWEARS_DATASET_PATH", "")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
SQLITE_DB_PATH = os.environ.get("SQLITE_DB_PATH", "db.sqlite")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=LOG_LEVEL
)

swears_dataset = utils.get_dataset(SWEARS_DATASET_PATH)


class CustomCallbackContext(CallbackContext):
    db = Database(SQLITE_DB_PATH)

    def __init__(self, *args, **kwargs):
        super(CustomCallbackContext, self).__init__(*args, **kwargs)


def get_random_swear(*args, **kwargs):
    return utils.get_random_choice(swears_dataset)


REPLY_METHODS = [get_random_swear, rhymer.get_rhyme]


def should_reply(update: Update, context: CustomCallbackContext):
    if not utils.random_bool():
        logging.debug("%s: random exit -> False", update.update_id)
        return False

    reply = context.db.get_reply_for_chat_id(update.message.chat.id)
    if reply.timeout < TIMEOUT_SEC:
        logging.debug("%s: timeout exit -> False", update.update_id)
        return False

    if reply.chat_id == update.message.from_user.id:
        logging.debug("%s: duplicate user exit -> False", update.update_id)
        return False
    return True


def reply_handler(update: Update, context: CustomCallbackContext) -> None:
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
            context.db.update_reply(update.message.chat.id, update.message.from_user.id)
        else:
            logging.debug("Reply message is empty")


if __name__ == "__main__":
    bot = Bot(token=BOT_TOKEN)
    bot_info = bot.get_me()
    logging.info("Inited bot %s @%s", bot.first_name, bot.username)

    # Create the Updater and pass it your bot's token.
    updater = Updater(
        bot=bot, context_types=ContextTypes(context=CustomCallbackContext)
    )

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Reply the message on Telegram only for groups
    dispatcher.add_handler(MessageHandler(Filters.chat_type.groups, reply_handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
