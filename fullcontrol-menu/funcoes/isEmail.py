import sys
import re


def isEmail(email):
    if len(email) > 7:
        if re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) != None:
            return True
    return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("""
isEmail is an e-mail validator
Use: isEmail example@example.com
              """)
        exit(-1)
    if isEmail(sys.argv[1]) == True:
        print('This is a valid e-mail address')
    else:
        print('This is not a valid e-mail address')
