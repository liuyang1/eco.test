from math import *
from scipy.stats import norm
import matplotlib.pylab as plt

x = [0.01*(i+1) for i in range(250)]
y = [norm.cdf(i)-norm.cdf(-i) for i in x]
z = [(2/(1-i)) for i in y]


plt.subplot(2, 1, 1)
plt.plot(x, y)
plt.subplot(2, 1, 2)
plt.plot(x, z)
#plt.show()
plt.savefig('1.png')
