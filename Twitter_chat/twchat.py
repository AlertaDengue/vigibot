import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET_KEY'))
auth.set_access_token(os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth)