import unittest
from vigibot.botdb import save_question
from dotenv import load_dotenv
load_dotenv()

class TestQuestions(unittest.TestCase):
    def test_save_question(self):
        save_question("Esta pergunta é um teste", "Twitter", 'fccoelho', 0)


if __name__ == '__main__':
    unittest.main()
