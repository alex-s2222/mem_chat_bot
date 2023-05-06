import logging

import telegram
from loguru import logger
import requests as re
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, callbackcontext
from moviepy.editor import ImageClip, concatenate_videoclips, VideoFileClip, ImageSequenceClip, CompositeVideoClip
import numpy as np
import cv2
import io
import os

URL = 'https://api.telegram.org/bot'
API_KEY = 'AIzaSyCBG9WPX4KvEsx1W40ihTjAjtciHn083xA'


bot = telegram.Bot(TOKEN)


def start(update: Update, context: callbackcontext) -> None:
    keyboard = [['/ address', '/number']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)

    update.message.reply_text(f'Привет {update.message.from_user.full_name}.'
                              f' Я хрюшка, потому что повторюшка', reply_markup=markup)


def close_keyboard(update: Update, context: callbackcontext) -> None:
    update.message.reply_text('Ok', reply_markup=ReplyKeyboardRemove())


def address(update: Update, context: callbackcontext) -> None:
    update.message.reply_text('я не знаю где ты живешь -_-, но в будущем я'
                              'сделаю за тобой слежку(не благодари)')
    update.message.reply_text(f'chat_id{update.message.chat.id}')


def number(update: Update, context: callbackcontext) -> None:
    update.message.reply_text(f'{update.message.from_user.full_name}')


def help_command(update: Update, context: callbackcontext) -> None:
    update.message.reply_text('SORRY I DONT андерстенд')


def echo(update: Update, context: callbackcontext) -> None:
    db_images = []
    if update.message.text[-1] == '?':
        update.message.reply_text('Я не могу отвечать на вопросы я только повторбшка :с')
    else:
        for i in update.message.text.split():
            # get_pictures(CHAT_ID=update.effective_chat.id, word=i)
            db_images.append(get_pictures(i))

    clips = []
    for i in db_images:
        clips.append(ImageClip(i).set_duration(2))

    final_clip = concatenate_videoclips(clips, method='compose')
    final_clip.write_videofile('test_py.mp4', fps=30)

    bot.send_animation(update.message.chat_id, open('test_py.mp4', 'rb'))


def get_pictures(word) -> list:
    GOOGLE_PICTURES = f'https://www.googleapis.com/customsearch/v1?cx=448c512f7ed8a5a3d&key={API_KEY}' \
                 f''f'&lr=lang_ru&searchType=image&q=' + word
    pictures = []
    for img in re.get(GOOGLE_PICTURES).json().get('items'):
        pictures.append(img.get('link'))

    Url_img = pictures[1]
    Content_img = re.get(Url_img)

    Frame = io.BytesIO(Content_img.content)
    Np_frame = np.frombuffer(Frame.getvalue(), np.uint8)

    image = cv2.imdecode(Np_frame, -1)
    return image


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
