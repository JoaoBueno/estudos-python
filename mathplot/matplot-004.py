import numpy as np
import matplotlib.pyplot as plt
import datetime as DT

data= np.loadtxt('daily_count.csv', delimiter=',', dtype={'names': ('date', 'count'),'formats': ('S10', 'i4')} )

x = [DT.datetime.strptime(key,'%Y-%m-%d') for (key, value) in data ]
y = [value for (key, value) in data]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()

fig.autofmt_xdate()

plt.plot(x,y,'b--o--')
plt.xlabel('Date')
plt.ylabel('Daily Count')
plt.title('Daily Count since February')
plt.show()