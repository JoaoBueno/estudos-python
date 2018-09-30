def numeros():
    yield 1
    yield 2
    yield 3


for i in numeros():
    print(i)
    print('\n')
