#!/usr/bin/python3

import os
import sys
import xmltodict

# caminho = sys.argv[1]
# caminho = r'P:\multidad\nfe'
caminho = r'/dados/sistema/multidad/nfe'

extens = ['xml', 'XML']

logname = 'arquivos-ok.log'
logerro = 'arquivos-er.log'
arq_imp = 'arq-imp.txt'

logarq = open(logname, 'w')
logerr = open(logerro, 'w')
arqimp = open(arq_imp, 'w')

found = {x: [] for x in extens}

conta = 0

for dirpath, dirnames, files in os.walk(caminho):
    for name in files:
        ext = name.lower().rsplit('.', 1)[-1]
        if ext in extens:
            conta += 1
            print(str(conta) + ' => ' + os.path.join(dirpath, name))
            with open(os.path.join(dirpath, name), 'rb') as arquivo:
                dados = arquivo.read().decode('UTF-8')
                doc = xmltodict.parse(dados)
                emp = ''
                des = ''
                fco = ''
                ver = ''
                esp = ''
                ser = ''
                num = ''
                nfe = ''
                arq = ''
                x = len(caminho) + 1
                emp = dirpath[x:x+2]
                if 'entrada' in dirpath:
                    des = 'entrada'
                elif 'saida' in dirpath:
                    des = 'saida'
                if (des == 'entrada') or (des == 'saida'):
                    if 'nfeProc' in doc:
                        try:
                            if des == 'entrada':
                                fco = doc['nfeProc']['NFe']['infNFe']['emit']['CNPJ']
                            else:
                                try:
                                    fco = doc['nfeProc']['NFe']['infNFe']['dest']['CNPJ']
                                except:
                                    try:
                                        fco = doc['nfeProc']['NFe']['infNFe']['dest']['CPF']
                                    except:
                                        fco = '1'
                            ver = doc['nfeProc']['NFe']['infNFe']['@versao']
                            if doc['nfeProc']['NFe']['infNFe']['ide']['mod'] == '55':
                                esp = 'NFE'
                            else:
                                esp = 'NFC'
                            ser = doc['nfeProc']['NFe']['infNFe']['ide']['serie']
                            num = doc['nfeProc']['NFe']['infNFe']['ide']['nNF']
                            nfe = doc['nfeProc']['NFe']['infNFe']['@Id'][3:]
                            arq = os.path.join(dirpath, name)
                            logarq.write('%s\n' % os.path.join(dirpath, name))
                        except:
                            logerr.write('%s\n' % os.path.join(dirpath, name))
                    elif 'procNFe' in doc:
                        try:
                            if des == 'entrada':
                                fco = doc['procNFe']['NFe']['infNFe']['emit']['CNPJ']
                            else:
                                try:
                                    fco = doc['procNFe']['NFe']['infNFe']['dest']['CNPJ']
                                except:
                                    try:
                                        fco = doc['procNFe']['NFe']['infNFe']['dest']['CPF']
                                    except:
                                        fco = '1'
                            ver = doc['procNFe']['NFe']['infNFe']['@versao']
                            if doc['procNFe']['NFe']['infNFe']['ide']['mod'] == '55':
                                esp = 'NFE'
                            else:
                                esp = 'NFC'
                            ser = doc['procNFe']['NFe']['infNFe']['ide']['serie']
                            num = doc['procNFe']['NFe']['infNFe']['ide']['nNF']
                            nfe = doc['procNFe']['NFe']['infNFe']['@Id'][3:]
                            arq = os.path.join(dirpath, name)
                            logarq.write('%s\n' % os.path.join(dirpath, name))
                        except:
                            logerr.write('%s\n' % os.path.join(dirpath, name))
                    else:
                        try:
                            if des == 'entrada':
                                fco = doc['NFe']['infNFe']['emit']['CNPJ']
                            else:
                                try:
                                    fco = doc['NFe']['infNFe']['dest']['CNPJ']
                                except:
                                    try:
                                        fco = doc['NFe']['infNFe']['dest']['CPF']
                                    except:
                                        fco = '1'
                            ver = doc['NFe']['infNFe']['@versao']
                            if doc['NFe']['infNFe']['ide']['mod'] == '55':
                                esp = 'NFE'
                            else:
                                esp = 'NFC'
                            ser = doc['NFe']['infNFe']['ide']['serie']
                            num = doc['NFe']['infNFe']['ide']['nNF']
                            nfe = doc['NFe']['infNFe']['@Id'][3:]
                            arq = os.path.join(dirpath, name)
                            logarq.write('%s\n' % os.path.join(dirpath, name))
                        except:
                            logerr.write('%s\n' % os.path.join(dirpath, name))
                    if arq != '':
                        emp.strip()
                        des.strip()
                        fco.strip()
                        ver.strip()
                        esp.strip()
                        ser.strip()
                        num.strip()
                        nfe.strip()
                        arq.strip()
                        # print(f'{emp};{des};{fco};{ver};{esp};{ser};{num};{nfe};{arq}\n')
                        # arqimp.write(f'{emp};{des};{fco};{ver};{esp};{ser};{num};{nfe};{arq}\n')
                        # print('{};{};{};{};{};{};{};{};{}\n'.format(emp, des, fco, ver, esp, ser, num, nfe, arq))
                        arqimp.write('{};{};{};{};{};{};{};{};{}\n'.format(emp, des, fco, ver, esp, ser, num, nfe, arq))

