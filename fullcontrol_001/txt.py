import os

f = open('lgd', 'r', errors='ignore')
g = open('lgg', 'w', errors='ignore')

l = 0
w = 0
for line in f:
    l = l + 1
    if int(l/1000) == l/1000:
        print('lidos ', l)
    if line[0:5] == '51VEN' or line[0:5] == '56VEN':
        g.write(line)
        w = w + 1
        if int(w/1000) == w/1000:
            print('gravados ', w)
