import scipy
import pylab 
import matplotlib.pyplot as plt

x,y = scipy.ogrid[-1.:1.:.01, -1.:1.:.01]
z = x**3-3*x*y**2
pylab.imshow(z, origin='lower', extent=[-1,1,-1,1])
plt.contour(z, origin='lower', extent=[-1,1,-1,1])
pylab.xlabel('x')
pylab.ylabel('y')
pylab.title('Saddle')
pylab.savefig('Saddle')
plt.show()