import unittest

from dotenv import load_dotenv

from vigibot.botdb import save_question

load_dotenv()


class TestQuestions(unittest.TestCase):
    def test_save_question(self):
        save_question("Esta pergunta é um teste", "Twitter", "fccoelho", 0)


if __name__ == "__main__":
    unittest.main()
