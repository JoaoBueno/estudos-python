import numpy as np 
a = np.array([[1,2],[3,4],[5,6]])
print(a)
b = a[1]
print(b)

for i,j in zip(range(4),range(4,8)):
    print(i,j)