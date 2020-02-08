import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import datetime

date = datetime.datetime.now()

# create message object instance


# conexão com o servidor
smtp_ssl_host = '1linha.com.br'
smtp_ssl_port = 587
# username ou email para logar no servidor
username = 'backup@1linha.com.br'
password = 'i!DZY8o3tk[m'

from_addr = 'backup@1linha.com.br'
to_addrs = ['bueno@1linha.com.br']

# a biblioteca email possuí vários templates
# para diferentes formatos de mensagem
# neste caso usaremos MIMEText para enviar
# somente texto
message = MIMEText('Backup ' + date.strftime("%d/%m/%Y"))
message['subject'] = 'Backup ' + date.strftime("%d/%m/%Y")
message['from'] = from_addr
message['to'] = ', '.join(to_addrs)

# Anexando o PDF
# message.attach(body)
# pdfname='em1.py'
# fp=open(pdfname,'rb')
# message.attach(MIMEText(fp.read().encode('utf8')),_subtype="txt")
# fp.close()

# anexo
message = MIMEMultipart()
message.attach('em1.py')
print(message)

# conectaremos de forma segura usando SSL
# server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
# server = smtplib.SMTP(f'{smtp_ssl_host}: {smtp_ssl_port}')
# server.starttls()
# # para interagir com um servidor externo precisaremos
# # fazer login nele
# server.login(username, password)
# server.sendmail(from_addr, to_addrs, message.as_string())
# server.quit()