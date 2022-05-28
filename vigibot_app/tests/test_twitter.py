import unittest
import random
from vigibot.twitter_client import api


class TwitterTestCase(unittest.TestCase):
    def test_send_update(self):
        word = random.choice(['turma', 'Turma', 'galera', 'Galera', 'amigx', 'Amigx', 'amigxs', 'Amigxs'])
        msg = f"Ola {word}! visitem o Infodengue: info.dengue.mat.br"
        api.update_status(msg)
        public_tweets = api.home_timeline()
        tweets = [tw.text for tw in public_tweets]
        self.assertIn(msg, tweets)


if __name__ == '__main__':
    unittest.main()
