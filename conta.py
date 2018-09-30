import sys
from random import randint
from random import gammavariate
from ctypes import windll
windll.kernel32.SetConsoleMode(windll.kernel32.GetStdHandle(-11), 7)
show = lambda s: sys.stdout.write(s)

off = 0

fg_blk = 30
fg_red = 31
fg_gre = 32
fg_yel = 33
fg_blu = 34
fg_mag = 35
fg_cya = 36
fg_whi = 37

bk_blk = 40
bk_red = 41
bk_gre = 42
bk_yel = 43
bk_blu = 44
bk_mag = 45
bk_cya = 46
bk_whi = 47

def cor(b,f,bi,fi):
    """Cor\n
    b - background-collor\n
    f - foreground-collor\n
    bi- background intensity\n
    bi- background intensity"""
    if bi == 1:
        b += 60
    print("\x1b[%d;%d;%dm" %(fi,b,f), end="")

# def cls(b,f,bi,fi):
#     """Limpa a tela\n
#     b - background-collor\n
#     f - foreground-collor\n
#     bi- background intensity\n
#     bi- background intensity"""
#     if bi == 1:
#         b += 60
#     print("\x1b[%d;%d;%dm" %(fi,b,f), end="")
#     show("\x1b[H\x1b[J")

def cls():
    """Limpa a tela"""
    print("\x1b[H\x1b[J", end="")

# def prt(b,f,bi,fi,msg):
#     """Mostra uma mensagem\n
#     b - background-collor\n
#     f - foreground-collor\n
#     bi- background intensity\n
#     bi- background intensity\n
#     msg - mensagem"""
#     if bi == 1:
#         b += 60
#     print("\x1b[%d;%d;%dm%s"%(fi,b,f,msg), end="")

def prt(msg,l = -1,c = -1):
    """Mostra uma mensagem\n
    l - linha   (opcional)\n
    c - coluna  (opcional)"""
    if l >= 0 and c >= 0:
        print("\x1b[%d;%dH" %(l,c), end="")
    print("%s"%(msg), end="")

cor(44,33,1,1)
cls()
print("teste")
# cls(44,33,1,1)
# prt(44,33,1,1,"teste")

cor(44,33,0,1)
prt("",10,50)
print(randint(0, 9))

cor(44,34,0,1)
prt("teste2")
prt("teste2")
prt("teste2")
cor(bk_blu,fg_yel,0,1)
prt("teste",0,0)
prt("teste",1,1)
prt("teste",2,2)
prt("teste",3,3)
prt("teste",4,4)
prt("teste",4,9)
