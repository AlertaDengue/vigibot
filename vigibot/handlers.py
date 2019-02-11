from vigibot import loghandler, logformatter
import logging
from telegram.ext.dispatcher import run_async
from emoji import emojize, UNICODE_EMOJI_ALIAS

# Setup logging
module_logger = logging.getLogger(__name__)
module_logger.addHandler(loghandler)
module_logger.setLevel(logging.INFO)


# end of log section


def error(bot, update, error_msg):
    module_logger.warning('Update "{}" caused error: {}'.format(update, error_msg))

def get_user_command_and_name(update):
    usr_command = str(update.effective_message.text) if update.effective_message.text else 'None'
    usr_name = update.message.from_user.first_name
    if update.message.from_user.last_name:
        usr_name += ' ' + update.message.from_user.last_name
    if update.message.from_user.username:
        usr_name += ' (@' + update.message.from_user.username + ')'
    return usr_command, usr_name

@run_async
def bom_dia(bot, update):
    # module_logger.info("entrou em bom_dia")
    usr_chat_id = update.message.chat_id
    if update:
        usr_command, usr_name = get_user_command_and_name(update)

        module_logger.info(
            "Has received a command \"{}\" from user {}, with id {}".format(usr_command, usr_name, usr_chat_id))

    emoj = emojize(':smiley:', use_aliases=True)
    bot.send_message(usr_chat_id, "Bom dia! "+emoj, parse_mode="Markdown")
    module_logger.info("Said 'Bom dia!' to %s", usr_chat_id)
