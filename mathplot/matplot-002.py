import numpy
import pylab

t = numpy.arange(0.0, 1.0+0.01, 0.01)
s = numpy.cos(numpy.pi*4*t)
pylab.plot(t, s)
 
pylab.xlabel('time (s)')
pylab.ylabel('cos(4t)')
pylab.title('Simple cosine')
pylab.grid(True)
pylab.savefig('simple_cosine')

pylab.show()