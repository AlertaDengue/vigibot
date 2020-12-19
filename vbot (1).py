#!/usr/bin/env python3
from telegram.ext import Updater, Filters
from telegram.ext import CommandHandler, MessageHandler
from vigibot import logformatter, loghandler
import logging
import os

from vigibot.handlers import bom_dia, error, alerta, unknown, location
from dotenv import load_dotenv

load_dotenv()
# Load environment variables from .env
BOT_TOKEN = os.getenv('BOT_TOKEN')



# Setup logging
module_logger = logging.getLogger(__name__)
module_logger.addHandler(loghandler)
module_logger.setLevel(logging.INFO)
# end of log section


def main():
    module_logger.info("Vigibot starting...")
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # bot's error handler
    dispatcher.add_error_handler(error)

    # bot's command handlers
    ola_handler = CommandHandler('ola', bom_dia)
    dispatcher.add_handler(ola_handler)
    # ola_handler2 = CommandHandler('olá', bom_dia)
    # dispatcher.add_handler(ola_handler2)

    alerta_handler = CommandHandler('alerta', alerta, pass_args=True, pass_user_data=True)
    dispatcher.add_handler(alerta_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    location_handler = MessageHandler(Filters.location, location, pass_user_data=True)
    dispatcher.add_handler(location_handler)

    updater.start_polling()
    updater.idle()




if __name__ == '__main__':
    main()
