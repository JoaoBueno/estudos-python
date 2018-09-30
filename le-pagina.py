import urllib.request
import time

t0= time.time()
req = urllib.request.urlopen('http://1linha.com.br')
pageHtml = req.read()
t1 = time.time()
print(pageHtml)
print("Total time to fetch page : {} secondes".format(t1-t0))