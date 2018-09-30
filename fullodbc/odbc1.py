# import json
import pyodbc
import simplejson as json
cnxn = pyodbc.connect('DSN=p;UID=system')
cursor = cnxn.cursor()

data = []

# for row in cursor.tables():
#     print(row.table_name)

# columns = [column[3] for column in cursor.columns(table='aigelgcp')]
# print(columns)
columns = []
columns.append('cliente')
columns.append('nome')
columns.append('jurfis')
# print(columns)
# input()

# cols = cursor.columns(table='aimanrep')
# for col in cols:
#     # print(col)
#     print(col.column_name, ' ', col.type_name, ' ', col[6], ' ', col[8])
#     input()

# cursor.execute("select * from aigelgcp where lgc_resumo = 'S'")
cursor.execute("select distinct  fco_fco, fco_nome, fco_jurfis from aigefcop LEFT JOIN aigefccp ON fco_empresa = fcc_empresa and fco_fco = fcc_fco where fco_empresa = 51 and fco_eclien = 'X' and fco_credito <> 'C' and fcc_seque <> 55 and fcc_seque <> 56  and fcc_seque <> 57  and fcc_seque <> 58  and fcc_seque <> 59 and fcc_seque <> 60")
for row in cursor.fetchall():
    # print(row)
    # data.append([x for x in row]) 
    # data.append(list(row))
    data.append(dict(zip(columns,row)))
    # print(data)
    # input()

# print(data)
print(json.dumps(data, sort_keys=False, indent=4))