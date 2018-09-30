import random
import sys

ans = True

while ans:
    question = input("Who's your bias on BTS?: (press enter to quit)")

    answers = random.randint(1,7)

    print(answers)

    if question == "":
        sys.exit()
    elif answers == 1:
        print ("Jimin")
    elif answers == 2:
        print ("Yoongi")
    elif answers == 3:
        print ("Seokjin")
    elif answers == 4:
        print ("Namjoon")
    elif answers == 5:
        print ("Jungkook")
    elif answers == 6:
        print ("Taehyung")
    elif answers == 7:
        print ("Hoseok")
