import sys
from ctypes import windll
windll.kernel32.SetConsoleMode(windll.kernel32.GetStdHandle(-11), 7)
#set ansi(vt100) control code interpreted
#https://stackoverflow.com/questions/36760127/how-to-use-the-new-support-for-ansi-escape-sequences-in-the-windows-10-console
show = lambda s: sys.stdout.write(s)
for b in range(30, 38):
    for f in range(40, 48):
        print("\x1b[0;%d;%dm %d,%d \x1b[0m"% (b,f,b,f), end="")
    print()

for b in range(30, 38):
    for f in range(40, 48):
        print("\x1b[1;%d;%dm %d,%d \x1b[0m"% (b,f,b,f), end="")
    print()

input()
show("\x1b[40m")
show("\x1b[2J")
input()
show("\x1b[H\x1b[J")
input()