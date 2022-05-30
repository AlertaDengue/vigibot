import unittest
from Twitter_chat.twchat import get_bot

class TestChat(unittest.TestCase):
    def test_answer(self):
        bot = get_bot('evigilancia')
        ans = bot.get_response('Estou com dengue?').text
        self.assertIn('dengue', ans.lower())
        ans2 = bot.get_response('zika').text
        self.assertIn('zika', ans2.lower())
    def test_crazy_text(self):
        bot = get_bot('evigilancia')
        ans = bot.get_response('que doideira este tweet doido.').text
        self.assertIn('dengue', ans.lower())

    def test_pergunta_epidemiologia(self):
        bot = get_bot('evigilancia')
        ans = bot.get_response('O que é epidemiologia?').text
        self.assertIn('epidemiologia', ans.lower())

    def test_pergunta_covid(self):
        bot = get_bot('evigilancia')
        ans = bot.get_response('O que é covid19 ?').text
        self.assertIn('covid19', ans.lower())