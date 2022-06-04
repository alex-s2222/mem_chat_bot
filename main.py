import logging
from loguru import logger
import requests as re
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, callbackcontext

CHAT_ID = '402844537'
URL = 'https://api.telegram.org/bot'
API_KEY = 'AIzaSyCBG9WPX4KvEsx1W40ihTjAjtciHn083xA'


def start(update: Update, context: callbackcontext) -> None:
    keyboard = [['/ address', '/number']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)

    update.message.reply_text(f'Привет {update.message.from_user.full_name}. Я хрюшка, потому что повторюшка', reply_markup=markup)


def close_keyboard(update: Update, context: callbackcontext) -> None:
    update.message.reply_text('Ok', reply_markup=ReplyKeyboardRemove())


def address(update: Update, context: callbackcontext) -> None:
    update.message.reply_text('я не ебу где ты живешь -_-, но в будущем я'
                              'сделаю за тобой слежку(не благодари)')
    update.message.reply_text(f'chat_id{update.message.chat.id}')


def number(update: Update, context: callbackcontext) -> None:
    update.message.reply_text(f'{update.message.from_user.full_name}')


def help_command(update: Update, context: callbackcontext) -> None:
    update.message.reply_text('SORRY I DONT андерстенд')


def echo(update: Update, context: callbackcontext) -> None:
    if update.message.text[-1] == '?':
        update.message.reply_text('Я не могу отвечать на вопросы я только повторбшка :с')
    else:
        for i in update.message.text.split():
            get_pictures(word=i)


def get_pictures(word) -> None:
    GOOGLE_PICTURES = f'https://www.googleapis.com/customsearch/v1?cx=448c512f7ed8a5a3d&key={API_KEY}' \
                 f''f'&lr=lang_ru&searchType=image&q=' + word
    pictures = []
    for img in re.get(GOOGLE_PICTURES).json().get('items'):
        pictures.append(img.get('link'))

    re.get(f'{URL}5349612772:AAGYc8KZUolYZlwHsIAqDPiodR0CnfImnX4/sendPhoto?chat_id={CHAT_ID}&photo={pictures[0]}')



def main() -> None:
    updater = Updater("5349612772:AAGYc8KZUolYZlwHsIAqDPiodR0CnfImnX4")
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(CommandHandler('close', close_keyboard))
    dispatcher.add_handler(CommandHandler('number', number))
    dispatcher.add_handler(CommandHandler('address', address))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # цикл приема и обработки сообщений
    updater.start_polling()

    # завершение
    updater.idle()


if __name__ == '__main__':
    main()