import logging
import os
import random
from functools import lru_cache
from uuid import uuid4
import html, json
import traceback

import psycopg2
from emoji import emojize
from geopy.geocoders import Nominatim
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram import ParseMode

from vigibot import loghandler
from vigibot.chat.engine import get_bot
from vigibot.data import get_geocode, get_alerta
from vigibot.twitter_client import api as tweetapi
from vigibot.twitter_client import follow_all
from vigibot.botdb import get_ppg2_connection, save_question

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
disease_keyboard = [[KeyboardButton('/alerta ' + d + ' Rio de Janeiro')] for d in ['dengue', 'chikungunya', 'zika']]
disease_keyboard_markup = ReplyKeyboardMarkup(disease_keyboard, one_time_keyboard=True)

# Setup Chat Engine
chatbot = get_bot('Evigibot')

DEVELOPER_CHAT_ID = 159627190

def error(update, context):
    module_logger.error("Exception handling update: ", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)
    try:
        message = (
            f'An exception was raised while handling an update\n'
            f'<pre>update = {html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False))}'
            '</pre>\n\n'
            f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
            f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
            f'<pre>{html.escape(tb_string)}</pre>'
        )

        # Finally, send the message
        context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML)
    except Exception as e:
        context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=f"Problem sending traceback {e}", parse_mode=ParseMode.HTML)


def get_user_command_and_name(update):
    usr_command = str(update.effective_message.text) if update.effective_message.text else 'None'
    usr_name = update.message.from_user.first_name
    if update.message.from_user.last_name:
        usr_name += ' ' + update.message.from_user.last_name
    if update.message.from_user.username:
        usr_name += ' (@' + update.message.from_user.username + ')'
    return usr_command, usr_name


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
    update.message.reply_text('Siga-me no <a href="https://twitter.com/evigilancia2">Twitter!</a>',
                              parse_mode=ParseMode.HTML)
    module_logger.info("Said 'Bom dia!' to %s", usr_chat_id)
    if not check_user_exists(user.id):
        add_user(user)
        update.message.reply_text("Prazer em te conhecer! " + emoj)
        reply_markup = ReplyKeyboardMarkup([[location_keyboard]])
        update.message.reply_text("Eu sou o Vigibot, minha missão é manter você informad@ sobre as arboviroses!")
        update.message.reply_text(
            "Voce se importa de compartilhar sua localizaçao comigo? \nAssim posso te enviar informaçoes sobre o seu local!",
            reply_markup=reply_markup)
    follow_all()


def inlinequery(update, context):
    query = update.inline_query.query
    try:
        user = 'Unknown' if update.message is None else update.message.from_user.username
        save_question(query, 'Telegram', str(user), update.message.chat_id)
    except Exception as e:
        context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=f"Problem saving inline query: {e}",
                                 parse_mode=ParseMode.HTML)
    response = InputTextMessageContent(chatbot.get_response(query).text)
    result = [
        InlineQueryResultArticle(
            id=uuid4(), title="Answer", input_message_content=response
        ),
    ]
    update.inline_query.answer(result)


def alerta(update, context):
    usr_chat_id = update.message.chat_id
    if context.args == []:
        update.message.reply_text("Por favor especifique uma doença e uma cidade.\nPor exemplo: /alerta dengue niteroi")
        return
    doenca = context.args[0].lower()
    if doenca not in ['dengue', 'chik', 'chikungunya', 'zika']:
        update.message.reply_text("Escolha uma destas doenças:", reply_markup=disease_keyboard_markup)
        return
    cidade = ' '.join(context.args[1:])
    if doenca == 'chikungunya':
        doenca = 'chik'
    # print(doenca, cidade)
    module_logger.info("%s fez uma consulta de alerta sobre %s em %s", usr_chat_id, doenca, cidade)

    gc = get_geocode(cidade)
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
        "Estamos no nivel " + niveis[alrt[0]] + ", para a " + doenca + ", na semana " + str(alrt[1])[
                                                                                        -2:] + " em " + cidade + ".",
        parse_mode="Markdown")
    update.message.reply_text(
        f'Para maiores detalhes, consulte o <a href="https://info.dengue.mat.br/alerta/{gc}/dengue">Infodengue</a>.',
        parse_mode=ParseMode.HTML)
    word = random.choice(['turma', 'Turma', 'galera', 'Galera', 'amig@', 'Amig@', 'amig@s', 'Amig@s', 'gente', 'Gente'])
    try:
        tweetapi.update_status(
            f"Oi {word}, estamos no nivel {niveis[alrt[0]]}, para a {doenca} em {cidade}.\nPara maiores detalhes, consulte o https://info.dengue.mat.br/alerta/{gc}/dengue")
    except:
        module_logger.debug("failed sending tweet.")
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


# Utility functions

def check_user_exists(tid):
    # eng = get_engine(pool_size=1)
    # with eng.connect() as conexao:
    conexao = get_ppg2_connection()
    cursor = conexao.cursor()
    cursor.execute(f'select * from bot_users where telegram_uid={tid}')  # , {'tid': tid}))
    res = cursor.fetchone()
    return (res is not None)


def add_user(user):
    # eng = get_engine(pool_size=1)
    # with eng.connect() as conexao:
    conexao = get_ppg2_connection()
    cursor = conexao.cursor()
    cursor.execute(
        f'insert into bot_users(telegram_uid, first_name, last_name) values({user.id}, \'{user.first_name}\',\'{user.last_name}\');')


def add_location(user, location):
    # eng = get_engine(pool_size=1)
    # with eng.connect() as conexao:
    conexao = get_ppg2_connection()
    cursor = conexao.cursor()
    sql = f"update bot_users set latitude= {location.latitude}, longitude= {location.longitude} where telegram_uid= {user.id};"
    cursor.execute(sql)


@lru_cache(maxsize=1000)
def get_location_from_coords(lat, lon):
    geolocator = Nominatim(user_agent="E-vigilancia")
    location = geolocator.reverse(f"{lat}, {lon}")
    return location
