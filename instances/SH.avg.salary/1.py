#! /usr/bin/env python2


from matplotlib.pyplot import *


year = range(1993,2019)
salary = [471, 617, # 1993, 1994
        773, 889, 952, 1005, 1179, # 1995-1999
        1285, 1480, 1623, 1847, 2033, # 2000-2004
        2235, 2464, 2892, 3292, 2566, # 2005-2009
        3896, 4331, 4692, 5036, 5451, # 2010-2014
        5939, 6504, 7132, 7832]       # 2015-2019

ratio = [1] + [salary[i+1] / (salary[i] + 0.0) for i in range(len(salary) - 1)]
print ratio

subplot(311)
plot(year, salary, "o--")
grid()

subplot(312)
semilogy(year, salary, "o--")
grid()

subplot(313)
plot(year, ratio)
grid()

# show()
savefig('1.png')
