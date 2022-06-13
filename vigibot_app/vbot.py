#!/usr/bin/env python3
import logging
import os

from dotenv import load_dotenv
from telegram.ext import (
    ChosenInlineResultHandler,
    CommandHandler,
    Filters,
    InlineQueryHandler,
    MessageHandler,
    Updater,
)

from vigibot import loghandler
from vigibot.handlers import (
    alerta,
    bom_dia,
    error,
    inlinequery,
    location,
    on_inline_result_chosen,
    unknown,
)

load_dotenv()
# Load environment variables from .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

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
    ola_handler = CommandHandler("ola", bom_dia, run_async=True)
    dispatcher.add_handler(ola_handler)
    # ola_handler2 = CommandHandler('olá', bom_dia)
    # dispatcher.add_handler(ola_handler2)

    alerta_handler = CommandHandler(
        "alerta", alerta, pass_args=True, pass_user_data=True, run_async=True
    )
    dispatcher.add_handler(alerta_handler)

    unknown_handler = MessageHandler(Filters.command, unknown, run_async=True)
    dispatcher.add_handler(unknown_handler)

    location_handler = MessageHandler(
        Filters.location, location, pass_user_data=True, run_async=True
    )
    dispatcher.add_handler(location_handler)

    dispatcher.add_handler(InlineQueryHandler(inlinequery, run_async=True))

    result_chosen_handler = ChosenInlineResultHandler(on_inline_result_chosen)
    dispatcher.add_handler(result_chosen_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
