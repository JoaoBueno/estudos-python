import os

# caminho = sys.argv[1]
caminho = r'P:\multidad\nfe'

extens = ['xml', 'XML']

found = {x: [] for x in extens}  

for dirpath, dirnames, files in os.walk(caminho):
    for name in files:
        ext = name.lower().rsplit('.', 1)[-1]
        if ext in extens:
            print(os.path.join(dirpath, name))

