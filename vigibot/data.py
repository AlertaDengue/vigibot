from sqlalchemy import create_engine, text
import pandas as pd
import os, re
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

db_engine = create_engine("postgresql://{}:{}@{}/{}".format(
    os.getenv('PSQL_USER'),
    os.getenv('PSQL_PASSWORD'),
    os.getenv('PSQL_HOST'),
    os.getenv('PSQL_DB')
))


def get_alerta_table(municipio=None, state=None, doenca='dengue'):
    """
    Pulls the data from a single city, cities from a state or all cities from the InfoDengue
    database
    :param doenca: 'dengue'|'chik'|'zika'
    :param municipio: geocode (one city) or None (all)
    :param state: full name of state, with first letter capitalized: "Cear
    :return: Pandas dataframe
    """
    estados = {'RJ': 'Rio de Janeiro', 'ES': 'Espírito Santo', 'PR': 'Paraná', 'CE': 'Ceará'}
    if state in estados:
        state = estados[state]
    conexao = create_engine("postgresql://{}:{}@{}/{}".format(config('PSQL_USER'),
                                                              config('PSQL_PASSWORD'),
                                                              config('PSQL_HOST'),
                                                              config('PSQL_DB')))
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

        df = pd.read_sql_query(sql, conexao, index_col='id')
    else:
        df = pd.read_sql_query(
            'select * from "Municipio"."{}" where municipio_geocodigo={} ORDER BY "data_iniSE" ASC;'.format(tabela,
                                                                                                            municipio),
            conexao, index_col='id')
    df.data_iniSE = pd.to_datetime(df.data_iniSE)
    df.set_index('data_iniSE', inplace=True)
    conexao.dispose()
    return df


def get_city_names(geocodigos):
    """
    Fetch names of the cities from a list of geocodes.
    :param geocodigos: list of 7-digit geocodes.
    :return:
    """
    with db_engine.connect() as conexao:
        res = conexao.execute(
            'select geocodigo, nome from "Dengue_global"."Municipio" WHERE geocodigo in {};'.format(tuple(geocodigos)))
        res = res.fetchall()

    return res


def get_alerta(geocodigo, doenca='dengue'):
    if doenca == 'dengue':
        tabela = 'Historico_alerta'
    elif doenca == 'chik':
        tabela = 'Historico_alerta_chik'
    elif doenca == 'zika':
        tabela = 'Historico_alerta_zika'
    with db_engine.connect() as conexao:
        res = conexao.execute(
            f'select nivel, "SE", municipio_geocodigo from "Municipio"."{tabela}" WHERE municipio_geocodigo={geocodigo} ORDER BY "data_iniSE" DESC limit 1;'
        )
        res = res.fetchone()

    return res


@lru_cache(maxsize=800)
def get_geocode(muname):
    """
    returns the geocode for a city name
    :param muname: name of the city
    :return: geocode (str)
    """
    # replace accents by '_' because Postgresql will accept any character for the position
    # muname = re.sub(r'[^\x00-\x7F]','_', muname)
    l = len(muname)
    with db_engine.connect() as conexao:
        gc = []
        while not gc:
            muname = muname[:l]
            res = conexao.execute(
                text('select geocodigo, nome from "Dengue_global"."Municipio" WHERE nome ilike :search'),
                {"search": f"{muname}%"}
            )
            gc = res.fetchall()
            l -= 1
            if l<3:
                return gc

        gc = gc[0][0]
        return gc
