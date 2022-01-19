# importing all required libraries
# import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
  
   
# get your api_id, api_hash, token
# from telegram as described above

# bueno
# api_id = 5585466
# api_hash = 'aa8b3de02af96d6c8a18b262774ce755'
# token = '1861042665:AAHNM8K9T5coicud3rxuaJSjIaahJGSakbs'

# compras
api_id = 4888068
api_hash = '16af559125cab1310194e8015672dce1'
token = '1612101465:AAGrCmHM86jDJRH-biquYs0ymmb_MoXS8j4'
  
# your phone number
# phone = '+5561982246622'
phone = '+55 61 99983 6707'
   
# creating a telegram session and assigning
# it to a variable client
client = TelegramClient('primeiralinhacompras_bot', api_id, api_hash)
   
# connecting and building the session
print(client.connect())
  
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
   
try:
    # receiver user_id and access_hash, use
    # my user_id and access_hash for reference
    # id_destino = client.get_input_entity('primeiralinha_bot')
    # id_destino = client.get_input_entity('+55 61 99405 3164')
    # id_destino = client.get_input_entity('+55 61 99983 6707')
    id_destino = client.get_input_entity('+55 (61) 98224-6622')
    # print(user_id)

  
    # sending message using telegram client
    # client.send_message(receiver, message='teste', parse_mode='html')
    mensagem="""Olá isso é um teste"""

    client.send_message(id_destino, message=mensagem, parse_mode='html')
    # client.send_file(id_destino, 's:\logo.png')
except Exception as e:
      
    # there may be many error coming in while like peer
    # error, wwrong access_hash, flood_error, etc
    print(e);
  
# disconnecting the telegram session 
client.disconnect()