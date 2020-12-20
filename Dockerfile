FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir git+git://github.com/gunthercox/chatterbot-corpus.git
RUN python -m spacy download en
RUN python -m spacy download pt

COPY . .

CMD [ "python", "./vbot.py" ]