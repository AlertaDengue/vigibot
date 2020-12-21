from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


def get_bot(name):
    chatbot = ChatBot(name,
                      logic_adapters=[
                          {
                              'import_path': 'chatterbot.logic.BestMatch',
                              'default_response': 'Não entendi. Me pergunte algo sobre dengue, zika ou chikungunya. https://info.dengue.mat.br',
                              'maximum_similarity_threshold': 0.90
                          }
                      ]
                      )
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train('corpora.portuguese')
    return chatbot
