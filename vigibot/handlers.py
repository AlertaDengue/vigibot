from vigibot import loghandler, logformatter
from vigibot.data import get_geocode, get_alerta
import logging
from telegram.ext.dispatcher import run_async
from telegram import KeyboardButton, ReplyKeyboardMarkup
from emoji import emojize, UNICODE_EMOJI_ALIAS

# Setup logging
module_logger = logging.getLogger(__name__)
module_logger.addHandler(loghandler)
module_logger.setLevel(logging.INFO)
# end of log section
uni_emoji = {
    'yellow_circle': '\U0001F7E1',
    'orange_circle': '\U0001F7ED',
    'green_circle': '\U0001F7E2',
    'red_circle': '\U0001F534',
    'thinking': '\U0001F914',
    'mosquito': '\U0001F99F'
}

location_keyboard = KeyboardButton(text="send_location", request_location=True)

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
def bom_dia(update, context):
    # module_logger.info("entrou em bom_dia")
    usr_chat_id = update.message.chat_id
    if update:
        usr_command, usr_name = get_user_command_and_name(update)

        module_logger.info(
            "Has received a command \"{}\" from user {}, with id {}".format(usr_command, usr_name, usr_chat_id))

    emoj = emojize(':smiley:', use_aliases=True)
    update.message.reply_text("Bom dia! " + emoj, parse_mode="Markdown")
    module_logger.info("Said 'Bom dia!' to %s", usr_chat_id)
    reply_markup = ReplyKeyboardMarkup([[location_keyboard]])
    update.message.reply_text("Voce pode compartilhar sua localizaçao comigo? \nAssim posso te enviar informaçoes sobre o seu local!", reply_markup=reply_markup)


@run_async
def alerta(update, context):
    usr_chat_id = update.message.chat_id

    # if update:
    #     usr_command, usr_name = get_user_command_and_name(update)
    doenca = context.args[0]
    cidade = ' '.join(context.args[1:])
    # print(doenca, cidade)
    module_logger.info("%s fez uma consulta de alerta sobre %s em %s", usr_chat_id, doenca, cidade)
    gc = get_geocode(cidade)
    # print(gc)
    if not isinstance(gc, int):
        update.message.reply_text(emojize(uni_emoji['thinking'])+" Nao conheço a cidade %s. Voce digitou os acentos?", cidade)
        module_logger.debug("falhou!")
        return
    alrt = get_alerta(gc, doenca)
    if alrt is None:
        update.message.reply_text(emojize(uni_emoji['thinking'])+" Nao temos esta informaçao no momento.")
        return
    # print(alrt)
    niveis = {1: "verde "+emojize(uni_emoji['green_circle']),
              2: "amarelo "+emojize(uni_emoji['yellow_circle']),
              3: "laranja "+emojize(uni_emoji['orange_circle']),
              4: "vermelho "+emojize(uni_emoji['red_circle']),
              }
    # update.message.reply_text("teste")
    update.message.reply_text(
        "Estamos no nivel " + niveis[alrt[0]] + ", para a " + doenca + ", na semana " + str(alrt[1])[-2:], parse_mode="Markdown")
    module_logger.info("Enviou alerta para %s", usr_chat_id)


def unknown(update, context):
    emoj = emojize(':smiley:', use_aliases=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Desculpa, Nao conheço este comando. " + emoj,
                             parse_mode="Markdown")

def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    module_logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                user_location.longitude)
    update.message.reply_text(emojize(':thumbs_up:', use_aliases=True)+ '\nObrigado! \nagora posso te informar sobre a situaçao na sua cidade!'
                              )

    return 1
