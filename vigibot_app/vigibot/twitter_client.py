import os

import tweepy
from dotenv import load_dotenv
from tweepy.errors import TweepyException

load_dotenv()

auth = tweepy.OAuthHandler(
    os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_SECRET_KEY")
)
auth.set_access_token(
    os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
)

api = tweepy.API(auth)


def follow_all():
    """
    Follow followers no tweeter
    """
    for follower in tweepy.Cursor(api.followers).items():
        try:
            follower.follow()
        except TweepyException:
            pass
