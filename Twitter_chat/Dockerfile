FROM python:3-alpine

WORKDIR /usr/src/app

COPY ../requirements.txt ./
COPY ../corpora/ ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en
RUN python -m spacy download pt

COPY . .

CMD [ "python", "./twchat.py" ]