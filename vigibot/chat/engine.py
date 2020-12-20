from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

def get_bot(name):
    chatbot = ChatBot(name)
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train('corpora.portuguese')
    return chatbot