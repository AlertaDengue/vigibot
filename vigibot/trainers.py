from chatterbot.trainers import Trainer
from chatterbot import languages
from chatterbot.tagging import PosLemmaTagger
from chatterbot.conversation import Statement
from chatterbot import utils
import os

class InfodengueCorpusTrainer(Trainer):
    """
    Allows the chat bot to be trained using data from the
    Infodengue corpus.
    """

    def train(self, *corpus_paths):
        from chatterbot.corpus import load_corpus, list_corpus_files

        tagger = PosLemmaTagger(language=languages.POR)

        data_file_paths = []

        # Get the paths to each file the bot will be trained with
        for corpus_path in corpus_paths:
            data_file_paths.extend(list_corpus_files(corpus_path))

        for corpus, categories, file_path in load_corpus(*data_file_paths):

            statements_to_create = []

            # Train the chat bot with each statement and response pair
            for conversation_count, conversation in enumerate(corpus):

                if self.show_training_progress:
                    utils.print_progress_bar(
                        'Training ' + str(os.path.basename(file_path)),
                        conversation_count + 1,
                        len(corpus)
                    )

                previous_statement_text = None
                previous_statement_search_text = ''

                for text in conversation:

                    statement_search_text = tagger.get_text_index_string(text)

                    statement = Statement(
                        text=text,
                        search_text=statement_search_text,
                        in_response_to=previous_statement_text,
                        search_in_response_to=previous_statement_search_text,
                        conversation='training'
                    )

                    statement.add_tags(*categories)

                    statement = self.get_preprocessed_statement(statement)

                    previous_statement_text = statement.text
                    previous_statement_search_text = statement_search_text

                    statements_to_create.append(statement)

            if statements_to_create:
                self.chatbot.storage.create_many(statements_to_create)