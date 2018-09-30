import sys
import pyodbc

cnxn = pyodbc.connect('DSN=p;UID=system')
cursor = cnxn.cursor()
data = []
columns = []
columns.append('cliente')
columns.append('nome')
columns.append('email')

# cursor.execute("select nfc_data, nfc_especie, nfc_serie, nfc_numero from aivenfcp \
# where nfc_empresa = 51 and nfc_fco = 24907602000519 and nfc_serie = '2' and nfc_opefis = 28 or nfc_opefis = 77")

for row in cursor.execute(
    "select nfc_data, nfc_especie, nfc_serie, nfc_numero, nre_ident from aivenfcp left join aimanrep on nfc_fco = nre_fco and nfc_serie = nre_serie and nre_especie = nre_especie and nfc_numero = nre_numdoc 
    where nfc_empresa = 51 and nre_empresa = 56 and nfc_fco = 24907602000519 and nfc_especie <> 'VEN' and nfc_opefis = 28 and nre_numdoc is NULL"):
    print(row)

# rows = cursor.fetchall()
# conta = 0
# lidos = 0
# for row in rows:
#     # lidos+=1
#     print(row)
#     # conta+=1

