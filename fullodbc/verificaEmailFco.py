import sys
import re
import pyodbc

def isEmail(email):
    """Verifica se o email -e valido"""
    if not re.match(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])", email):
        return(False)
    return(True)        

cnxn = pyodbc.connect('DSN=p;UID=system')
cursor = cnxn.cursor()
data = []
columns = []
columns.append('cliente')
columns.append('nome')
columns.append('email')
cursor.execute("select fco_fco, fco_nome, fco_email from aigefcop where fco_empresa = 51 and fco_email <> ''")
rows = cursor.fetchall()
conta = 0
lidos = 0
for row in rows:
    lidos+=1
    if not isEmail(row[2]):
        print(row[0], row[1], row[2])
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
