# http://www.bogotobogo.com/python/python_matplotlib.php

import matplotlib.pyplot as pyp
x = [0, 2, 4, 6, 8, 9, 11]
y = [0, 3, 3, 7, 0, 11, 12]
pyp.plot(x, y)
pyp.savefig("MyFirstPlot.png")