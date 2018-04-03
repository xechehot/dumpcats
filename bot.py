import sys
import os
import time
import telepot
import telepot.namedtuple
from telepot.loop import MessageLoop
from tempfile import TemporaryFile

from fastai.transforms import *
from fastai.conv_learner import *
from fastai.model import *

import numpy as np



def open_image(file_object):
    flags = cv2.IMREAD_UNCHANGED + cv2.IMREAD_ANYDEPTH + cv2.IMREAD_ANYCOLO
    img_array = np.asarray(bytearray(file_object.read()), dtype=np.uint8)
    im = cv2.imdecode(img_array, cv2_img_flag).astype(np.float32)/255
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)


def transformed_image(file_object):
    image = open_image(file_object)
    _, val_tfms = tfms_from_model(resnet34, 224)
    source_img = open_image(image)
    return val_tfms(source_img)


def predict(file_object):
    image = transformed_image(file_object)

    tm = torch.load(PATH + 'dogs-cats-torch-model.pt',
                    map_location=lambda storage, loc: storage)
    tm.train(False)

    x = Variable(torch.from_numpy(image), requires_grad=False)
    output = tm(x.cpu())
    return np.exp(output.cpu().data.numpy())


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    m = telepot.namedtuple.Message(**msg)

    # print(m.photo)

    # import ipdb; ipdb.set_trace();

    # if chat_id < 0:
    #     # group message
    #     print('Received a %s from %s, by %s' % (content_type, m.chat, m.from_))
    # else:
    #     # private message
    #     print('Received a %s from %s' % (content_type, m.chat))  # m.chat == m.from_

    if content_type == 'photo':
        f = TemporaryFile('wb')
        if len(m.photo) < 2:
            reply = "Photo too small!"
        else:
            bot.download_file(m.photo[1].file_id, f)
            reply = predict(f)

        bot.sendMessage(chat_id, reply)


TOKEN = os.environ["BOT_TOKEN"]

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
