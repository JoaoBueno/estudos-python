import sys
import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description = 'Envia mensagens pelo Telegram')
    parser.add_argument('-m', '--message', dest='message', help='Mensagem a ser enviada', required=True)
    parser.add_argument('-p', '--phones', dest='phones', help='Telefones destino', required=True)
    options = parser.parse_args()
    return options


options = get_arguments()

print(options)

if not (options.message):
    print('Precisa ser uma hora valida, exemplo: 01:45')
    exit(-1)

if not (options.phones):
    print('Precisa ser uma hora valida, exemplo: 01:45')
    exit(-1)
    