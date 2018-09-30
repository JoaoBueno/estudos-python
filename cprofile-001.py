# -*- coding: latin1 -*-
import cProfile
def rgb1():
    """
    Função usando range()
    """
    rgbs = []
    for r in range(256):
        for g in range(256):
            for b in range(256):
                rgbs.append('#%02x%02x%02x' % (r, g, b))
    return rgbs

def rgb2():
    """
    Função usando range()
    """
    rgbs = []
    for r in range(256):
        for g in range(256):
            for b in range(256):
                rgbs.append('#%02x%02x%02x' % (r, g, b))
    return rgbs

def rgb3():
    """
    Gerador usando range()
    """
    for r in range(256):
        for g in range(256):
            for b in range(256):
                yield '#%02x%02x%02x' % (r, g, b)

def rgb4():
    """
    Função usando uma lista várias vezes
    """
    rgbs = []
    ints = range(256)
    for r in ints:
        for g in ints:
            for b in ints:
                rgbs.append('#%02x%02x%02x' % (r, g, b))
    return rgbs

def rgb5():
    """
    Gerador usando apenas uma lista
    """
    for i in range(256 ** 3):
        yield '#%06x' % i

def rgb6():
    """
    Gerador usando range() uma vez
    """
    for i in range(256 ** 3):
        yield '#%06x' % i

# Benchmarks
print('rgb1:')
cProfile.run('rgb1()')
print('rgb2:')
cProfile.run('rgb2()')
print('rgb3:')
cProfile.run('list(rgb3())')
print('rgb4:')
cProfile.run('rgb4()')
print('rgb5:')
cProfile.run('list(rgb5())')
print('rgb6:')
cProfile.run('list(rgb6())')