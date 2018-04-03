FROM paperspace/fastai:cuda9_pytorch0.3.0

RUN mkdir /app

ADD requirements.txt /app/
RUN pip install -r /app/requirements.txt

ADD . /app/

WORKDIR /app/
CMD python bot.py

