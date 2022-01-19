from twilio.rest import Client
import os

# as credenciais são recuperadas das variáveis de ambiente TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
client = Client()

print(client)

# esse é o numero de teste da sandbox da Twilio
from_whatsapp_number='whatsapp:+14155238886'
# substitua esse número com o seu próprio número do Whatsapp
to_whatsapp_number='whatsapp:+15005550006'

client.messages.create(body='Ahoy, world!',
                      from_=from_whatsapp_number,
                      to=to_whatsapp_number)
