#!/usr/bin/python
import psycopg2
from config import config


def connect():
    ''' Connect to the PostgreSQL database server '''
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # # execute a statement
        # print('PostgreSQL database version:')
        # cur.execute('SELECT version()')

        # # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)

        # # close the communication with the PostgreSQL
        # cur.close()
        return conn, cur
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()
    #         print('Database connection closed.')


if __name__ == '__main__':
    conn, cur = connect()

    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)

    festrutura = open('aicup026.est', 'r')
    eestrutura = festrutura.read().replace('TABCUBO', 'aicup026').replace(
        'CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')

    print(eestrutura)

    try:
        cur.execute(eestrutura)
        print('tabela criada')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    conn.commit()

    i = 0
    with open('aicup026.sql', 'r', encoding="ISO-8859-1") as fsql:
        esql = fsql.readline().replace('TABCUBO', 'aicup026')
        while esql:
            # print(esql)
            esql = fsql.readline().replace('TABCUBO', 'aicup026')
            try:
                cur.execute(esql)
                i += 1
                print(i)
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

    conn.commit()
