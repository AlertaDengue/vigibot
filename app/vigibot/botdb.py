"""
Access functions to the Vigibot database
"""
import os
from os.path import dirname, join

import psycopg2
from dotenv import load_dotenv

env_file = os.environ.get("ENV_FILE", ".env")
dotenv_path = join(dirname(dirname(dirname(__file__))), env_file)
load_dotenv(dotenv_path)


def get_ppg2_connection():
    db_config = {
        "database": os.getenv('PSQL_BOTDB'),
        "user": os.getenv('PSQL_USER'),
        "password": os.getenv('PSQL_PASSWORD'),
        "host": os.getenv('PSQL_HOST'),
        "port": os.getenv('PSQL_PORT'),
    }

    return psycopg2.connect(**db_config)


def create_pergunta_table():
    conn = get_ppg2_connection()
    with conn.cursor() as cur:
        cur.execute(
            "select * from information_schema.tables where table_name='pergunta' limit 5;"
        )
        if not cur.rowcount:
            cur.execute(
                'create table pergunta(id bigserial, username varchar(32), network varchar(16), pergunta text, datetime timestamp, msgid bigint;'
            )


def save_question(pergunta, rede, userid, msgid):
    conn = get_ppg2_connection()
    with conn.cursor() as cursor:
        sql = f"insert into pergunta(network,username,pergunta,msgid) values('{rede}','{userid}','{pergunta}',{msgid});"
        cursor.execute(sql)
    conn.commit()


def is_new_id(msgid):
    conn = get_ppg2_connection()
    with conn.cursor() as cursor:
        sql = f'select msgid from pergunta where msgid={msgid};'
        cursor.execute(sql)
        res = cursor.fetchall()
    return len(res) == 0
