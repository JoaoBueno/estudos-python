import json

TABLE_NAME = "estados"

sqlstatement = ''
with open('estados.json', 'r') as f:
    jsondata = json.loads(f.read())

t = {}

for json in jsondata:
    keylist = "("
    valuelist = "("
    firstPair = True
    for key, value in json.items():
        if not firstPair:
            keylist += ", "
            valuelist += ", "
        firstPair = False
        keylist += key
        if type(value) in (str, str):
            valuelist += "'" + value + "'"
        else:
            valuelist += str(value)
    keylist += ")"
    valuelist += ")"

    sqlstatement += "INSERT INTO " + TABLE_NAME + " " + keylist + " VALUES " + valuelist + "\n"

print(sqlstatement)
