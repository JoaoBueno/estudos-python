import csv

reader = csv.DictReader(open('b-co.csv'), delimiter='|')
dictobj = next(reader) 

print(reader)
print(dictobj)

print(dictobj['NUMERO'])

# for row in reader:
#     print(row)