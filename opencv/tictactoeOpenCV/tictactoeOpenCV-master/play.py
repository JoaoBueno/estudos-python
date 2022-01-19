#
# Jogo da Velha utilizando Visao Computacional e Realidade aumentada.
# Definicao de funcoes auxiliares
#

import numpy as np


# Funcao que verifica se e o fim do jogo.
def won(tabuleiro):
    if (tabuleiro[0] == tabuleiro[1] == tabuleiro[2] == 0):
        return 1
    elif (tabuleiro[0] == tabuleiro[3] == tabuleiro[6] == 0):
        return 1
    elif (tabuleiro[6] == tabuleiro[7] == tabuleiro[8] == 0):
        return 1
    elif (tabuleiro[2] == tabuleiro[5] == tabuleiro[8] == 0):
        return 1
    elif (tabuleiro[3] == tabuleiro[4] == tabuleiro[5] == 0):
        return 1
    elif (tabuleiro[1] == tabuleiro[4] == tabuleiro[7] == 0):
        return 1
    elif (tabuleiro[0] == tabuleiro[4] == tabuleiro[8] == 0):
        return 1
    elif (tabuleiro[2] == tabuleiro[4] == tabuleiro[6] == 0):
        return 1

    elif (tabuleiro[0] == tabuleiro[1] == tabuleiro[2] == 1):
        return 2
    elif (tabuleiro[0] == tabuleiro[3] == tabuleiro[6] == 1):
        return 2
    elif (tabuleiro[6] == tabuleiro[7] == tabuleiro[8] == 1):
        return 2
    elif (tabuleiro[2] == tabuleiro[5] == tabuleiro[8] == 1):
        return 2
    elif (tabuleiro[3] == tabuleiro[4] == tabuleiro[5] == 1):
        return 2
    elif (tabuleiro[1] == tabuleiro[4] == tabuleiro[7] == 1):
        return 2
    elif (tabuleiro[0] == tabuleiro[4] == tabuleiro[8] == 1):
        return 2
    elif (tabuleiro[2] == tabuleiro[4] == tabuleiro[6] == 1):
        return 2

    else:
        if -1 not in tabuleiro:
            return 3
        else:
            return 0


# Realiza um movimento em uma posicao livre no tabuleiro.
def move(tabuleiro, posicao, peca):
    if tabuleiro[posicao] == -1:
        tabuleiro[posicao] = peca



# funcao para localizar os cantos do tabuleiro.
def canto(y1, x1, y2, x2, y3, x3, y4, x4, h, w, k):
    if k == "TL":
        yc, xc = 0, 0
    if k == "TR":
        yc, xc = 0, w
    if k == "BL":
        yc, xc = h, 0
    if k == "BR":
        yc, xc = h, w

    d1 = np.sqrt(np.power(y1-yc,2)+ np.power(x1-xc,2))
    d2 = np.sqrt(np.power(y2-yc,2)+ np.power(x2-xc,2))
    d3 = np.sqrt(np.power(y3-yc,2)+ np.power(x3-xc,2))
    d4 = np.sqrt(np.power(y4-yc,2)+ np.power(x4-xc,2))
    d = [d1,d2,d3,d4]

    if min(d) == d1:
        return 0
    if min(d) == d2:
        return 1
    if min(d) == d3:
        return 2
    if min(d) == d4:
        return 3



# funcao utilizada para ordenar os pontos do tabuleiro.
# Utilizada para auxiliar na transformacao de perspectiva.
def ordena(aprox, shape):
    ord = np.copy(aprox)
    h,w = shape

    y1,x1 = aprox[0][0][0],aprox[0][0][1]
    y2,x2 = aprox[1][0][0],aprox[1][0][1]
    y3,x3 = aprox[2][0][0],aprox[2][0][1]
    y4,x4 = aprox[3][0][0],aprox[3][0][1]

    TL = canto(y1, x1, y2, x2, y3, x3, y4, x4, h, w, "TL")
    TR = canto(y1, x1, y2, x2, y3, x3, y4, x4, h, w, "TR")
    BL = canto(y1, x1, y2, x2, y3, x3, y4, x4, h, w, "BL")
    BR = canto(y1, x1, y2, x2, y3, x3, y4, x4, h, w, "BR")

    ord[1] = aprox[TL]
    ord[3] = aprox[TR]
    ord[0] = aprox[BL]
    ord[2] = aprox[BR]

    return ord
