import logging
import os
import time

import tweepy
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from dotenv import load_dotenv
from tweepy.error import TweepError

load_dotenv()
logger = logging.getLogger()
with open('keywords') as k:
    keywords = k.readlines()


def get_bot(name):
    chatbot = ChatBot(name)
    trainer = ChatterBotCorpusTrainer(chatbot)
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
            time.sleep(5 * 60)


def follow_followers(api):
    logger.info("Retrieving and following followers")
    for follower in limit_handled(tweepy.Cursor(api.followers).items()):
        if not follower.following:
            logger.info(f"Following {follower.name}")
            try:
                follower.follow()
            except TweepError as e:
                pass


def reply_mentions(api, keywords, since_id, bot):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in limit_handled(tweepy.Cursor(api.mentions_timeline,
                               since_id=since_id).items()):
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")

            if not tweet.user.following:
                tweet.user.follow()

            api.update_status(
                status=bot.get_response(tweet.text).text,
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id


def main():
    api = create_api()
    chatbot = get_bot('Evigibot')
    since_id = 1
    while True:
        follow_followers(api)
        logger.info("Waiting...")
        time.sleep(60)
        reply_mentions(api, keywords, since_id=since_id, bot=chatbot)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
