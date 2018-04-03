FROM digitalgenius/ubuntu-pytorch

RUN mkdir /app

ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt

ADD . /app/

WORKDIR /app/
CMD python3 bot.py

