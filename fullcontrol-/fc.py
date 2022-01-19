#!/usr/bin/python
if __name__ == '__main__':

    i = 0
    with open('aicup026.sql', 'r', encoding="ISO-8859-1") as fsql:
        esql = fsql.readline().replace('TABCUBO', 'aicup026')
        while esql:
            print(esql)
            a = esql.split(',')
            print(a)
            input()
            esql = fsql.readline().replace('TABCUBO', 'aicup026')
