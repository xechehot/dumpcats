import sys
import os
import time
import telepot
import telepot.namedtuple
from telepot.loop import MessageLoop
import io


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

        f = io.BytesIO()
        if len(m.photo) < 2:
            reply = "Photo too small!"
        else:
            bot.download_file(m.photo[1].file_id, f)
            reply = f.tell()

        bot.sendMessage(chat_id, reply)


TOKEN = os.environ["BOT_TOKEN"]

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
