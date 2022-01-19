#!/usr/bin/python3

import argparse
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events


def get_arguments():
    parser = argparse.ArgumentParser(description = 'Envia mensagens pelo Telegram')
    parser.add_argument('-p', '--phones', dest='phones', help='Telefones destino', required=True)
    parser.add_argument('-m', '--message', dest='message', help='Mensagem a ser enviada', required=True)
    options = parser.parse_args()
    return options


def connect():
    # compras
    api_id = 4888068
    api_hash = '16af559125cab1310194e8015672dce1'
    token = '1612101465:AAGrCmHM86jDJRH-biquYs0ymmb_MoXS8j4'
    
    # your phone number
    phone = '+55 61 99983 6707'
    
    # creating a telegram session and assigning
    # it to a variable client
    client = TelegramClient('primeiralinhacompras_bot', api_id, api_hash)
    
    # connecting and building the session
    client.connect()
    
    # in case of script ran first time it will
    # ask either to input token or otp sent to
    # number or sent or your telegram id 
    if not client.is_user_authorized():
    
        client.send_code_request(phone)
        
        # signing in the client
        client.sign_in(phone)
        try:
            client.sign_in(code=input('Enter code: '))
        except: 
            client.sign_in(password='070707')
    
    return client

def send_message(client, target, message):
    try:
        id_destino = client.get_input_entity(target)
    
        client.send_message(id_destino, message=message, parse_mode='html')
        # client.send_file(id_destino, 's:\logo.png')
        return 'ok'
    except Exception as e:
        return e
  

options = get_arguments()

client = connect()

for phone in options.phones.split(', '):
    send_message(client, phone, options.message)

# disconnecting the telegram session 
client.disconnect()
