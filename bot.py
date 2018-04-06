# coding=utf-8
import sys
import time
import telepot
import telepot.namedtuple
from telepot.loop import MessageLoop
from tempfile import TemporaryFile
import os
import io
from model import CatDogPredictor


def get_handle(predictor):
    def handle(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        m = telepot.namedtuple.Message(**msg)

        if content_type == 'photo':
            f = io.BytesIO()
            if len(m.photo) < 2:
                reply = "Картинка слишком мала"
            else:
                bot.download_file(m.photo[1].file_id, f)
                cat, dog = predictor.predict(f)
                reply = "Котик 🐱: {:.2%}\nСобачка 🐶: {:.2%}".format(cat, dog)

            bot.sendMessage(chat_id, reply)
        else:
            bot.sendMessage(chat_id, "Пришли мне картинку! 🏞")
    return handle
    
TOKEN = os.environ["BOT_TOKEN"]
predictor = CatDogPredictor('/app/dogs-cats-torch-model.pt')
bot = telepot.Bot(TOKEN)
MessageLoop(bot, get_handle(predictor)).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
