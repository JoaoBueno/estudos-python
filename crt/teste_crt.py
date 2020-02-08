import sys
import crt
from ctypes import windll
windll.kernel32.SetConsoleMode(windll.kernel32.GetStdHandle(-11), 7)

crt.cor(44,33,1,1)
crt.cls()
print("teste")

crt.cor(44,33,0,1)
crt.prt("",10,50)
# print(randint(0, 9))

crt.cor(44,34,0,1)
crt.prt("teste2")
crt.prt("teste2")
crt.prt("teste2")
crt.cor(crt.bk_blu,crt.fg_yel,0,1)
crt.prt("teste",0,0)
crt.prt("teste",1,1)
crt.prt("teste",2,2)
crt.prt("teste",3,3)
crt.prt("teste",4,4)
crt.prt("teste",4,9)
