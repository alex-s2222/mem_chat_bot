import logging
from loguru import logger

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, callbackcontext


def start(update: Update, context: callbackcontext) -> None:
    user = update.effective_user
    Update.MESSAGE.reply_markdown_v2(
        fr'Hi{user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: callbackcontext) -> None:
    update.message.reply_text('Help!')


def echo(update: Update, context: callbackcontext) -> None:
    logger.info(f'Ответ')
    update.message.reply_text(f'Ответ: {update.message.text}')


def main() -> None:
    updater = Updater("5349612772:AAGYc8KZUolYZlwHsIAqDPiodR0CnfImnX4")

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()