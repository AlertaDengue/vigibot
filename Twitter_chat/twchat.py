import logging
import os
import sys
import time

import tweepy
from chatterbot import ChatBot
from vigibot.trainers import InfodengueCorpusTrainer
from vigibot.botdb import save_question, is_new_id
from dotenv import load_dotenv
from tweepy.error import TweepError
import random

load_dotenv()
logger = logging.getLogger(name="Twitter chat")
logger.addHandler(logging.StreamHandler(sys.stdout))

pth = os.path.split(__file__)[0]
with open(os.path.join(pth, 'keywords')) as k:
    keywords = k.readlines()

infodengue_urls = ['https://info.dengue.mat.br',
                   'https://info.dengue.mat.br/informacoes/',
                   'https://info.dengue.mat.br/alerta/CE/chikungunya',
                   'https://info.dengue.mat.br/alerta/CE/dengue',
                   'https://info.dengue.mat.br/alerta/CE/zika',
                   'https://info.dengue.mat.br/alerta/MG',
                   'https://info.dengue.mat.br/alerta/ES',
                   'https://info.dengue.mat.br/alerta/MA/dengue',
                   'https://info.dengue.mat.br/alerta/PR/dengue',
                   'https://info.dengue.mat.br/alerta/SC/dengue',
                   ]


def get_bot(name):
    chatbot = ChatBot(name,
                      logic_adapters=[
                          {
                              'import_path': 'chatterbot.logic.BestMatch',
                              'default_response': 'Não entendi. Me pergunte algo sobre dengue, zika ou chikungunya, ou visite:',
                              'maximum_similarity_threshold': 0.95
                          }
                      ],
                      storage_adapter='chatterbot.storage.SQLStorageAdapter',
                      database_uri='sqlite:///db.sqlite3'
                      )
    trainer = InfodengueCorpusTrainer(chatbot)
    trainer.train('corpora.portuguese')
    return chatbot


def create_api():
    auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET_KEY'))
    auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

    api = tweepy.API(auth)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except (tweepy.RateLimitError, StopIteration):
            time.sleep(60)


def reply_mentions(api, keywords, since_id, Cbot):
    logger.info("Retrieving mentions")
    # print("Checking mentions")
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline,
                               since_id=since_id).items():
        if not is_new_id(int(tweet.id)):  # check if this tweet has already been answered.
            continue
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        # if any(keyword in tweet.text.lower() for keyword in keywords):
        #     logger.info(f"Answering to {tweet.user.name}")
        if tweet.text.startswith('Peguei dos amigos do @evigilancia2'):
            continue
        msg = tweet.text.lstrip('@evigilancia2').lower()
        try:
            save_question(msg, 'Twitter', tweet.user.screen_name, tweet.id)
        except Exception as e:
            logger.error(f"Não consegui salvar mensagem {msg} do Twitter:\n {e}")
        ans = f'@{tweet.user.screen_name} ' + Cbot.get_response(msg).text
        if ans.endswith('ou visite:'):
            ans += random.choice(infodengue_urls)
        logger.info(f"Pergunta: {msg}, Resposta: {ans}")
        # print(msg)
        # print(ans)
        # print(tweet.id, tweet.user.screen_name)
        if not tweet.user.following:
            tweet.user.follow()
        try:
            api.update_status(
                status=ans,
                in_reply_to_status_id=tweet.id,
            )
        except TweepError as e:
            logger.error(f'Could not reply: {e}')

    return new_since_id


def main():
    api = create_api()
    chatbot = get_bot('Evigilancia')
    since_id = 1
    while True:
        since_id = reply_mentions(api, keywords, since_id=since_id, Cbot=chatbot)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
