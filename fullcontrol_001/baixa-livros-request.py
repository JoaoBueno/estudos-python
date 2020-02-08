import datetime
import requests
from bs4 import BeautifulSoup as bs
import time
import re

# LINK DA PAGINA
link = "https://www.packtpub.com/packt/offers/free-learning?from=block"

# CABECALHO WEB(USER-AGENT)
cabe = {
    'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'}

# MANDANDO REQUESICAO
requesicao = requests.get(link, headers=cabe)

# PEGANDO A SOURCE
objeto = bs(requesicao.text, 'html.parser')

# PEGANDO O TITULO
titulo = objeto.find('div', class_='dotd-title').find('h2').text

# PEGANDO A DATA
tempo = objeto.find(
    'div', class_="eighteen-days-countdown-bar").find('span').get('data-countdown-to')

# TRADUZINDO A DATA


def get_date(utc_offset):
    utc_offset = int(utc_offset) * 1000
    now = datetime.datetime.utcnow()
    # Vai TNC!!! Tive que dar um sambarilove na hora...
    h = ((now.hour + 2) * 3600000)
    m = (now.minute * 60000)
    s = (now.second * 1000)
    timeLeft = int(86400000) - (int(h) + int(m) + int(s)) - int(utc_offset)
    milliseconds = int((timeLeft % 1000) / 100)
    seconds = int((timeLeft / 1000) % 60)
    minutes = int((timeLeft / (1000 * 60)) % 60)
    hours = int((timeLeft / (1000 * 60 * 60)) % 24)
    hours = "0" + str(hours) if (hours < 10) else hours
    minutes = "0" + str(minutes) if (minutes < 10) else minutes
    seconds = "0" + str(seconds) if (seconds < 10) else seconds
    tempo = "" + str(hours) + ":" + str(minutes) + ":" + str(seconds)
    return tempo


tempo1 = get_date(tempo)

# REGEX
titulo = re.sub(r'\s\s+', ' ', (re.sub(r'^\s+$|\n', '', titulo)))

# IMPRIMINDO TUDO
print('\nTitulo:', titulo, '\nData:', tempo1, '\nLink:', link)
