import sys
import csv


def processa(f):
    """
    Le arquivo e transforma em excel
    """
    arqOk = False
    for line in f:
        if arqOk:
            print(line, end='')
        else:
            if "[toExcel]" in line:
                arqOk = True


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Use: leArq-001 arquivo")
        sys.exit(0)
    try:
        # with open(sys.argv[1], 'r') as f:
        with open(sys.argv[1], 'r') as f:
            spamreader = csv.reader(f, delimiter=';', quotechar='|')
            for row in spamreader:
                for ele in row:
                    print(ele.strip())
            # processa(f)
    except IOError:
        print(u'Arquivo não encontrado!')
    sys.exit()
