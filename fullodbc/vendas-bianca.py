import sys
import pyodbc

cnxn = pyodbc.connect('DSN=p;UID=system')
cursor = cnxn.cursor()
data = []
columns = []
columns.append('pedido')
columns.append('vendedor')
columns.append('data')
columns.append('hora')
columns.append('horai')
cursor.execute("select * from aivevecp where (vec_empresa = 51 or vec_empresa = 53 or vec_empresa = 56) and vec_repre = 538 and vec_serie <> 'TRF' and vec_status <> 'C' and vec_terminal = 8")
rows = cursor.fetchall()
conta = 0
lidos = 0
for row in rows:
    lidos+=1
    # print(row[0], row[1], row[2], row[3], row[4])
    print(row)
    conta+=1

print('Lidos {}, invalidos {}'.format(lidos, conta))

# print(rows)
# for row in cursor.fetchall():
#     # print(row)
#     # data.append([x for x in row])
#     # data.append(list(row))
#     print(row[0][0])
#     data.append(dict(zip(columns,row)))
#     print(data)
#     input()

# email = "bueno@1linha"
# if not re.match(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])", email):
#     print("email invalido")
