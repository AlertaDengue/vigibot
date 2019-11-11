from vigibot import loghandler, logformatter
from vigibot.data import get_geocode, get_alerta
import logging, os
from sqlalchemy import create_engine, text
from telegram.ext.dispatcher import run_async
from telegram import ParseMode
from telegram import KeyboardButton, ReplyKeyboardMarkup
from emoji import emojize, UNICODE_EMOJI_ALIAS
from geopy.geocoders import Nominatim
from functools import lru_cache

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
disease_keyboard = [[KeyboardButton('/alerta '+d+' Rio de Janeiro')] for d in ['dengue','chikungunya','zika']]
disease_keyboard_markup = ReplyKeyboardMarkup(disease_keyboard, one_time_keyboard=True)

botdb_engine = create_engine("postgresql://{}:{}@{}/{}".format(
    os.getenv('PSQL_USER'),
    os.getenv('PSQL_PASSWORD'),
    os.getenv('PSQL_HOST'),
    os.getenv('PSQL_BOTDB')
))


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
    user = update.message.from_user
    usr_chat_id = update.message.chat_id
    if update:
        usr_command, usr_name = get_user_command_and_name(update)

        module_logger.info(
            "Has received a command \"{}\" from user {}, with id {}".format(usr_command, usr_name, usr_chat_id))

    emoj = emojize(':smiley:', use_aliases=True)
    update.message.reply_text("Bom dia! " + user.first_name + emoj, parse_mode="Markdown")
    module_logger.info("Said 'Bom dia!' to %s", usr_chat_id)
    if not check_user_exists(user.id):
        reply_markup = ReplyKeyboardMarkup([[location_keyboard]])
        update.message.reply_text("Eu sou o Vigibot, minha missão é manter você informadx sobre as arboviroses!")
        update.message.reply_text(
            "Voce se importa de compartilhar sua localizaçao comigo? \nAssim posso te enviar informaçoes sobre o seu local!",
            reply_markup=reply_markup)

        add_user(user)

@run_async
def inlinequery(update, context):
    query = update.inline_query.query

@run_async
def alerta(update, context):
    usr_chat_id = update.message.chat_id
    if context.args == []:
        update.message.reply_text("Por favor especifique uma doença e uma cidade.\nPor exemplo: /alerta dengue niteroi")
        return
    doenca = context.args[0]
    if doenca not in ['dengue', 'chik', 'chikungunya', 'zika']:
        update.message.reply_text("Escolha uma destas doenças:", reply_markup=disease_keyboard_markup)
        return
    cidade = ' '.join(context.args[1:])
    if doenca == 'chikungunya':
        doenca = 'chik'
    # print(doenca, cidade)
    module_logger.info("%s fez uma consulta de alerta sobre %s em %s", usr_chat_id, doenca, cidade)
    gc = get_geocode(cidade)
    # print(gc)
    if not isinstance(gc, int):
        update.message.reply_text(
            emojize(uni_emoji['thinking']) + " Nao conheço a cidade \"" + cidade + "\". Voce digitou os acentos?")
        module_logger.debug("falhou!")
        return
    alrt = get_alerta(gc, doenca)
    if alrt is None:
        update.message.reply_text(emojize(uni_emoji['thinking']) + " Nao temos esta informaçao no momento.")
        return
    # print(alrt)
    niveis = {1: "verde ",
              2: "amarelo ",
              3: "laranja ",
              4: "vermelho ",
              }

    update.message.reply_text(
        "Estamos no nivel " + niveis[alrt[0]] + ", para a " + doenca + ", na semana " + str(alrt[1])[-2:]+" em "+cidade+".",
        parse_mode="Markdown")
    update.message.reply_text(
        f'Para maiores detalhes, consulte o <a href="https://info.dengue.mat.br/alerta/{gc}/dengue">Infodengue</a>.',
        parse_mode=ParseMode.HTML)

    module_logger.info("Enviou alerta para %s", usr_chat_id)


def unknown(update, context):
    emoj = emojize(':smiley:', use_aliases=True)
    update.message.reply_text("Desculpa, Nao conheço este comando. " + emoj,
                             parse_mode="Markdown")


def location(update, context):
    user = update.message.from_user
    user_location = update.message.location
    module_logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                       user_location.longitude)
    update.message.reply_text(emojize(':thumbs_up:', use_aliases=True) + '\nObrigado ' + user.first_name + \
                              '\nagora posso te informar sobre a situaçao na sua cidade!'
                              )
    add_location(user, user_location)


def check_user_exists(tid):
    with botdb_engine.connect() as conexao:
        res = conexao.execute(f'select * from bot_users where telegram_uid={tid}')  # , {'tid': tid}))
        res = res.fetchone()
    return (res is not None)


def add_user(user):
    with botdb_engine.connect() as conexao:
        conexao.execute(
            f'insert into bot_users(telegram_uid, first_name, last_name) values({user.id}, \'{user.first_name}\',\'{user.last_name}\');')


def add_location(user, location):
    with botdb_engine.connect() as conexao:
        sql = text("update bot_users set latitude= :lat, longitude= :long where telegram_uid= :id;")
        conexao.execute(sql, **{'lat': location.latitude, 'long': location.longitude, 'id': user.id})


@lru_cache(maxsize=1000)
def get_location_from_coords(lat, lon):
    geolocator = Nominatim(user_agent="E-vigilancia")
    location = geolocator.reverse(f"{lat}, {lon}")
    return location
