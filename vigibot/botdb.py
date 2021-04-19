"""
Access functions to the Vigibot database
"""
import psycopg2
import os
from data import get_ppg2_connection


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
