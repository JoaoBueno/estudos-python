import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as md

data= np.loadtxt('vmstat_7days_without_header.csv', delimiter=',',
    dtype={'names': ['time', 'mon','tue','wed','thrs','fri','sat','sun'],
           'formats': ['S8','i4','i4','i4','i4','i4','i4','i4']} )

x,y1,y2,y3,y4,y5,y6,y7 = [],[],[],[],[],[],[],[]

for z in data:
# 10 minute span
    # print(z[0].decode("utf-8"))
    # print(int(z[0].split(':',2))[1])

    if int((z[0].decode("utf-8").split(':',2))[1]) % 10 == 0:
        xc = dt.datetime.strptime(z[0].decode("utf-8"),"%H:%M:%S")
        x.append(xc)
        y1.append(z[1])
        y2.append(z[2])
        y3.append(z[3])
        y4.append(z[4])
        y5.append(z[5])
        y6.append(z[6])
        y7.append(z[7])

fig = plt.figure()
ax = fig.add_subplot(111)
xfmt = md.DateFormatter('%H')
ax.xaxis.set_major_formatter(xfmt)
ax.grid()

# slanted x-axis tick label
fig.autofmt_xdate()

p1 = plt.plot(x,y1,'rs')
p2 = plt.plot(x,y2,'gp')
p3 = plt.plot(x,y3,'b*')
p4 = plt.plot(x,y4,'ch')
p5 = plt.plot(x,y5,'mp')
p6 = plt.plot(x,y6,'ys')
p7 = plt.plot(x,y7,'kD')

plt.ylabel("CPU Idle [%]")
plt.xlabel("Time of the day[hr]")

plt.ylim(84.0, 101)

plt.title("CPU Load for 7 days (10min interval), Idling Time, from vmstat command")

# let python select the best position for legend
plt.legend((p1[0],p2[0],p3[0],p4[0],p5[0],p6[0],p7[0]), 
          ('Mon','Tue','Wed','Thu','Fri','Sat','Sun'))

plt.show()