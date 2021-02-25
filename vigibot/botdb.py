"""
Access functions to the Vigibot database
"""
import psycopg2
import os

def get_ppg2_connection():
    conn = psycopg2.connect(f"dbname={os.getenv('PSQL_BOTDB')} user={os.getenv('PSQL_USER')} "
                            f"host={os.getenv('PSQL_HOST')} password={os.getenv('PSQL_PASSWORD')}"
                            )
    return conn

def save_question(pergunta, rede, userid, msgid):
    conn = get_ppg2_connection()
    cursor = conn.cursor()
    sql = f"insert into pergunta(network,username,pergunta,msgid) values('{rede}','{userid}','{pergunta}',{msgid});"
    cursor.execute(sql)
    conn.commit()

def is_new_id(msgid):
    conn = get_ppg2_connection()
    cursor = conn.cursor()
    sql = f'select msgid from pergunta where msgid={msgid};'
    cursor.execute(sql)
    res = cursor.fetchall()
    return len(res) == 0
