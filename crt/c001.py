import sys
import time
from ctypes import windll
windll.kernel32.SetConsoleMode(windll.kernel32.GetStdHandle(-11), 7)

for r in range(250, 256):
    for g in range(0, 256):
        for b in range(0, 256):
            c = r * 256 + g * 16 + b
            code = str(r * 256 + g * 16 + b)
            # print(code)
            sys.stdout.write(u"\u001b[38;2;{};{};{}".format(r, g, b) + "m " + 
                             "#{}{}{}".format(hex(r)[2:].rjust(2), hex(g)[2:].rjust(2), hex(b)[2:].rjust(2)))
            if (c / 16 == c // 16) and (c > 0):
                print(u"\u001b[0m")
        print(u"\u001b[0m")
        input()

for i in range(0, 16):
    for j in range(0, 16):
        code = str(i * 16 + j)
        # sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
        # print(u"\u001b[38;5;" + code + "m " + code.rjust(4), end="")
    print(u"\u001b[0m")


for i in range(0, 16):
    for j in range(0, 16):
        code = str(i * 16 + j)
        sys.stdout.write(u"\u001b[48;5;" + code + "m " + code.ljust(4))
    print(u"\u001b[0m")

print(u"\u001b[1m\u001b[4m\u001b[7m BOLD Underline Reversed \u001b[0m")


def loading():
    print("Loading...")
    for i in range(0, 100):
        time.sleep(0.1)
        sys.stdout.write(u"\u001b[1000D" + str(i + 1) + "%")
        sys.stdout.flush()
    print()


loading()
