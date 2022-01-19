import requests
from bs4 import BeautifulSoup

def web(page,WebUrl):
        if(page>0):
            url = WebUrl
            code = requests.get(url)
            plain = code.text
            s = BeautifulSoup(plain, 'html.parser')
            print(s.prettify())
            print(list(s.chidren))
            for link in s.findAll('table', {'class':'MsoNormalTable'}):
                # print(link)
                tet = link.get('title')
                print(tet)
                tet_2 = link.get('href')
                print(tet_2)

web(1,'http://www.fazenda.df.gov.br/aplicacoes/legislacao/legislacao/TelaSaidaDocumento.cfm?txtNumero=82&txtAno=2018&txtTipo=7&txtParte=.')
