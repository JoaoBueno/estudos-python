import xmltodict

with open('nfe.xml', 'rb') as arquivo:
    dados = arquivo.read().decode('UTF-8')
    doc = xmltodict.parse(dados)
    print(doc['nfeProc']['NFe']['infNFe']['emit']['CNPJ'])
    print(doc['nfeProc']['NFe']['infNFe']['@versao'])
