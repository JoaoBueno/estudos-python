import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
account_sid = 'ACa67b281fe50d431059c3cbbaecce6b9d'
auth_token = 'd4e4842f3fe4298a9d49990a0f6b1188'
client = Client(account_sid, auth_token)

message = client.messages.create(
                              body='Fala Henry!',
                            #   from_='whatsapp:+5561982246622',
                            #   to='whatsapp:+5561999181788'
                              from_='whatsapp:+14155238886',
                              to='whatsapp:+556182246622'
                          )

print(message.sid)
print(message)
