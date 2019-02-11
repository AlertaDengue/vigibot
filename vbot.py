#!/usr/bin/env python3
from telegram.ext import Updater
from telegram.ext import CommandHandler
from vigibot import logformatter, loghandler
import logging

from vigibot.handlers import bom_dia, error
import dotenv

# Load environment variables from .env
dotenv.load()


# Setup logging
module_logger = logging.getLogger(__name__)
module_logger.addHandler(loghandler)
module_logger.setLevel(logging.INFO)
# end of log section

def main():
    module_logger.info("Tradebot starting...")
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    # bot's error handler
    dispatcher.add_error_handler(error)

    # bot's command handlers
    ola_handler = CommandHandler('ola', bom_dia, pass_args=True)
    dispatcher.add_handler(ola_handler)
    ola_handler2 = CommandHandler('olá', bom_dia, pass_args=True)
    dispatcher.add_handler(ola_handler)

    updater.start_polling()
    updater.idle()




if __name__ == '__main__':
    main()
