
with open('aicup026.sql', 'r') as fsql:
    esql = fsql.readline().strip().replace('TABCUBO', 'aicup026').replace("' ", "'").replace(" '", "'")
    a = esql.split(' ').split(',')
    print(a)
    a = input()
    while esql:
        print(esql)
        esql = fsql.readline().strip().replace('TABCUBO', 'aicup026').replace("' ", "'").replace(" '", "'")
        a = input('teste')