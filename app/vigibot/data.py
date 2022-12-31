import psycopg2
from sqlalchemy import create_engine, text
import pandas as pd
import os
import re
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    db_engine = create_engine("postgresql://{}:{}@{}/{}".format(
        os.getenv('PSQL_USER'),
        os.getenv('PSQL_PASSWORD'),
        os.getenv('PSQL_HOST'),
        os.getenv('PSQL_DB')
    ))
    return db_engine

def get_ppg2_connection():
    conn = psycopg2.connect(
        host=os.getenv('PSQL_HOST'),
        database=os.getenv('PSQL_DB'),
        user=os.getenv('PSQL_USER'),
        password=os.getenv('PSQL_PASSWORD')
    )
    return conn


def get_alerta_table(municipio=None, state=None, doenca='dengue'):
    """
    Pulls the data from a single city, cities from a state or all cities from the InfoDengue
    database
    :param doenca: 'dengue'|'chik'|'zika'
    :param municipio: geocode (one city) or None (all)
    :param state: full name of state, with first letter capitalized: "Cear
    :return: Pandas dataframe
    """
    # db_engine = get_engine()
    conn = get_ppg2_connection()
    estados = {'RJ': 'Rio de Janeiro',
               'ES': 'Espírito Santo', 'PR': 'Paraná', 'CE': 'Ceará'}
    if state in estados:
        state = estados[state]

    if doenca == 'dengue':
        tabela = 'Historico_alerta'
    elif doenca == 'chik':
        tabela = 'Historico_alerta_chik'
    elif doenca == 'zika':
        tabela = 'Historico_alerta_zika'
    if municipio is None:
        sql = 'select h.* from "Municipio"."{}" h JOIN "Dengue_global"."Municipio" m ON h.municipio_geocodigo=m.geocodigo where m.uf=\'{}\';'.format(
            tabela,
            state)

        df = pd.read_sql_query(sql, conn, index_col='id')
    else:
        df = pd.read_sql_query(
            'select * from "Municipio"."{}" where municipio_geocodigo={} ORDER BY "data_iniSE" ASC;'.format(tabela,
                                                                                                            municipio),
            conn, index_col='id')
    df.data_iniSE = pd.to_datetime(df.data_iniSE)
    df.set_index('data_iniSE', inplace=True)

    return df


def get_city_names(geocodigos):
    """
    Fetch names of the cities from a list of geocodes.
    :param geocodigos: list of 7-digit geocodes.
    :return:
    """
    # db_engine = get_engine()
    conn = get_ppg2_connection()
    with conn.cursor() as curs:
        curs.execute(
            f'select geocodigo, nome from "Dengue_global"."Municipio" WHERE geocodigo in {tuple(geocodigos)};')
        res = curs.fetchall()

    return res


def get_alerta(geocodigo, doenca='dengue'):
    if doenca == 'dengue':
        tabela = 'Historico_alerta'
    elif doenca == 'chik':
        tabela = 'Historico_alerta_chik'
    elif doenca == 'zika':
        tabela = 'Historico_alerta_zika'
    conn = get_ppg2_connection()
    with conn.cursor() as curs:
        curs.execute(
            f'select nivel, "SE", municipio_geocodigo from "Municipio"."{tabela}" WHERE municipio_geocodigo={geocodigo} ORDER BY "data_iniSE" DESC limit 1;'
        )
        res = curs.fetchone()

    return res


@lru_cache(maxsize=800)
def get_geocode(muname):
    """
    Returns the geocode for a city name
    :param muname: name of the city
    :return: geocode (str)
    """
    # replace accents by '_' because Postgresql will accept any character for the position
    # muname = re.sub(r'[^\x00-\x7F]','_', muname)
    l = len(muname)
    # db_engine = get_engine()
    conn = get_ppg2_connection()
    with conn.cursor() as curs:
        gc = []
        while not gc:
            muname = muname[:l]
            curs.execute(f'select geocodigo, nome from "Dengue_global"."Municipio" WHERE nome ilike \'{muname}\'')
            gc = curs.fetchall()
            l -= 1
            if l < 3:
                return gc

        gc = gc[0][0]
        return gc
