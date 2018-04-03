# coding=utf-8
import sys
import os
import time
import telepot
import telepot.namedtuple
from telepot.loop import MessageLoop
from tempfile import TemporaryFile

from fastai.imports import *
from fastai.transforms import *
from fastai.conv_learner import *
from fastai.model import *
from fastai.dataset import *
from fastai.sgdr import *
from fastai.plots import *

import cv2

import io
import numpy as np


def open_image(file_object):
    # flags = cv2.IMREAD_UNCHANGED + cv2.IMREAD_ANYDEPTH + cv2.IMREAD_ANYCOLO
    flags = 5
    file_object.seek(0)
    img_array = np.asarray(bytearray(file_object.read()), dtype=np.uint8)
    im = cv2.imdecode(img_array, flags).astype(np.float32) / 255
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)


def transformed_image(file_object):
    # image = open_image(file_object)
    _, val_tfms = tfms_from_model(resnet34, 224)
    source_img = open_image(file_object)
    return val_tfms(source_img)


def predict(file_object):
    image = transformed_image(file_object)

    tm = torch.load('/app/dogs-cats-torch-model.pt',
                    map_location=lambda storage, loc: storage)
    tm.train(False)
    print(image.shape)
    x = Variable(torch.from_numpy(np.array([image])), requires_grad=False)
    output = tm(x.cpu())
    return np.exp(output.cpu().data.numpy())[0]


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    m = telepot.namedtuple.Message(**msg)

    if content_type == 'photo':
        f = io.BytesIO()
        if len(m.photo) < 2:
            reply = "Картинка слишком мала"
        else:
            bot.download_file(m.photo[1].file_id, f)
            cat, dog = predict(f)
            reply = "Котик 🐱: {:.2%}\nСобачка 🐶: {:.2%}".format(cat, dog)

        bot.sendMessage(chat_id, reply)
    else:
        bot.sendMessage(chat_id, "Пришли мне картинку! 🏞")


TOKEN = os.environ["BOT_TOKEN"]

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
