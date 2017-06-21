import sys

years = [2010, 2011, 2012, 2013, 2014, 2015, 2016]
gdp_avg = [4300, 5000, 5870, 6740, 7380, 7820, 8280]

# ref: https://web.phb123.com/city/GDP/8770.html
# http://finance.qq.com/cross/20160119/xP46Z82D.html

rate = gdp_avg[-1] / (gdp_avg[0] + 0.0)
print rate

rate_per_year = rate ** (1. / (len(gdp_avg) - 1))
print rate_per_year

gdp_avg_2020 = gdp_avg[-1] * (rate_per_year ** (2020 - years[-1]))
print "from 2016 to 2020"
print gdp_avg_2020

# print "This speed is faster than GDP's" # ???

ring_ratio = [x1/(x0+0.0) for x0, x1 in zip(gdp_avg, gdp_avg[1:])]
ring_ratio.insert(0, 1)

print ring_ratio

# plot

fontsize = 10
import matplotlib.pyplot as pl
import pylab
pl.style.use('ggplot')

fig, ax = pl.subplots(nrows=3, ncols=1)

def plotDataYears(data, title):
    pl.plot(years, data)
    pl.title(title, fontsize = fontsize)
    locs,labels = pl.xticks()
    pl.xticks(locs, map(lambda x: "%g" % x, locs))

pl.subplot(311)
plotDataYears(gdp_avg, 'GDP average')

pl.subplot(312)
pl.semilogy(years, gdp_avg)
plotDataYears(gdp_avg, 'GDP average with logy')

pl.subplot(313)
plotDataYears(ring_ratio, 'GDP average ring ratio')

fig.tight_layout()
pylab.savefig('1.png')
