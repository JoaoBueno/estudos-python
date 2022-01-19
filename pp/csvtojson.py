import csv

csvfile = open('Pasta1.csv', 'r')
csvfiln = open('Pasta1-ok.csv', 'w')

# fieldnames = ('Centro', 'Material', 'Descrição do Material', 'sep', 'opcao', 'prog')
# reader = csv.DictReader(csvfile, fieldnames, delimiter=';')
reader = csv.DictReader(csvfile, delimiter=';')
c = 0
Centro = ''
Material = ''
Descricao = ''
Codigo = ''
tt = ''
for row in reader:
    if ((tt == '') or (tt == row['tt'])):
        Centro = row['Centro']
        Material = row['Material']
        Descricao = row['Descricao']
        Codigo = row['Codigo SKF']
        tt = row['tt']
        csvfiln.write(row['Centro'] + ';' +
                      row['Material'] + ';' +
                      row['Descricao'] + ';' +
                      row['Codigo SKF'] + ';' +
                      row['tt'] + ';;' +
                      chr(13))
    else:
        c = c + 1
        print(tt, c)
        csvfiln.write(';' +
                      ';' +
                      ';' +
                      ';' +
                      ';' +
                      str(c) + chr(13))
        if (Codigo != row['Codigo SKF']):
            c = 0
        Centro = row['Centro']
        Material = row['Material']
        Descricao = row['Descricao']
        Codigo = row['Codigo SKF']
        tt = row['tt']
        csvfiln.write(row['Centro'] + ';' +
                row['Material'] + ';' +
                row['Descricao'] + ';' +
                row['Codigo SKF'] + ';' +
                row['tt'] + ';;' +
                chr(13))


