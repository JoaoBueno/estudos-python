import mimetypes
import os
import smtplib
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from six.moves import configparser

def adiciona_anexo(msg, filename):
    if not os.path.isfile(filename):
        return
    ctype, encoding = mimetypes.guess_type(filename)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
        with open(filename) as f:
            mime = MIMEText(f.read(), _subtype=subtype)
    elif maintype == 'image':
        with open(filename, 'rb') as f:
            mime = MIMEImage(f.read(), _subtype=subtype)
    elif maintype == 'audio':
        with open(filename, 'rb') as f:
            mime = MIMEAudio(f.read(), _subtype=subtype)
    else:
        with open(filename, 'rb') as f:
            mime = MIMEBase(maintype, subtype)
            mime.set_payload(f.read())
        encoders.encode_base64(mime)
    mime.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(mime)

def envia_email(de, para, subject, email, anexo):
    '''
        envia_email
            de = string
            para = array de strings
            subject = string
            email = string
            anexo = array de strings
    '''

    cfg = configparser.ConfigParser()
    cfg.read('backup.ini')

    # conexão com o servidor
    smtp_ssl_host = cfg.get('backup', 'smtp_ssl_host')
    smtp_ssl_port = cfg.getint('backup', 'smtp_ssl_port')
    # username ou email para logar no servidor
    username = cfg.get('backup', 'username')
    password = cfg.get('backup', 'password')

    # de = 'backup@1linha.com.br'
    # para = ['bueno@1linha.com.br']
    msg = MIMEMultipart()
    msg['From'] = de
    msg['To'] = ', '.join(para)
    msg['Subject'] = subject
    # Corpo da mensagem
    msg.add_header('Content-Type', 'text/html')
    # msg.set_payload(email)
    # msg.attach(MIMEText('Backup ' + date.strftime("%d/%m/%Y"), 'html', 'utf-8'))
    msg.attach(MIMEText(email, 'html', 'utf-8'))
    # Arquivos anexos.
    for anx in anexo:
        adiciona_anexo(msg, anx)
    raw = msg.as_string()
    # smtp = smtplib.SMTP_SSL(‘smtp.gmail.com', 465)
    smtp = smtplib.SMTP('{smtp_ssl_host}: {smtp_ssl_port}'.format(smtp_ssl_host=smtp_ssl_host, 
                                                                  smtp_ssl_port=smtp_ssl_port))
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(de, para, raw)
    smtp.quit()