import sys
import pyodbc
import pandas as pd

cnxn = pyodbc.connect('DSN=p;UID=system')
cursor = cnxn.cursor()
data = []
columns = []
columns.append('pedido')
columns.append('vendedor')
columns.append('data')
columns.append('hora')
columns.append('horai')
# cursor.execute("select * from aivevecp where (vec_empresa = 51 or vec_empresa = 53 or vec_empresa = 56) and vec_repre = 538 and vec_serie <> 'TRF' and vec_status <> 'C' and vec_terminal = 8")
# cursor.execute("select * from aivevecp where (vec_empresa = 51 or vec_empresa = 53 or vec_empresa = 56) and vec_usuar <> 'balcao' and vec_usuar <> 'EDMILSON' and vec_repre <> 597 and vec_serie <> 'TRF' and vec_terminal = 8")
cursor.execute("""select * from aivevecp
                           where (vec_empresa = 51 or vec_empresa = 53 or vec_empresa = 56)
                           and vec_usuar <> 'balcao' and vec_repre <> 597
                           and vec_serie <> 'TRF' and vec_serie <> 'IMP'
                           and vec_data > '20211000'
                           and vec_terminal = 1""")
# rows = cursor.fetchall()

col_headers = [ i[0] for i in cursor.description ]
print(col_headers)

rows = [ list(i) for i in cursor.fetchall()] 
df = pd.DataFrame(rows, columns=col_headers)

df.to_csv("test.csv", index=False)

# conta = 0
# lidos = 0
# arq = open('vds-usu.csv', 'w')
# for row in cursor:
#     lidos+=1
#     print(row)
#     arq.write(row)
#     conta+=1

# print('Lidos {}, invalidos {}'.format(lidos, conta))



