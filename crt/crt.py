# Biblioteca de Configurações de video
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

def cls():
    """Limpa a tela"""
    print("\x1b[H\x1b[J", end="")

def prt(msg,l = -1,c = -1):
    """Mostra uma mensagem\n
    l - linha   (opcional)\n
    c - coluna  (opcional)"""
    if l >= 0 and c >= 0:
        print("\x1b[%d;%dH" %(l,c), end="")
    print("%s"%(msg), end="")
