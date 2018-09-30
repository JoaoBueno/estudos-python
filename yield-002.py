def impar(elems):
    for i in elems:
        if i % 2:
            yield i

for x in impar(range(1000)):
  print(x)    