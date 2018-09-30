import urllib.request
import time
from bs4 import BeautifulSoup

t0= time.time()
req = urllib.request.urlopen('http://1linha.com.br')
pageHtml = req.read()
t1 = time.time()
# print(pageHtml)
print("Total time to fetch page : {} seconds".format(t1-t0))

# soup = BeautifulSoup(req.read(), "html.parser")
soup = BeautifulSoup(pageHtml, 'html.parser')

for link in soup.find_all('a'):
    print(link.get('href'))

t2 = time.time()
print("Total execution time: {} seconds".format(t2-t1))
# print(soup.prettify())

print(soup.title)