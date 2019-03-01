import csv
import time
import datetime
import functools
import operator
import math
import sys


def str2date(s):
    d = time.strptime(s, "%Y-%m-%d")
    d = datetime.datetime.fromtimestamp(time.mktime(d))
    return d


def loadData():
    with open('../data/040040_20171024_20181024.txt', 'rb') as fp:
        # rd = csv.reader(csvfile, delimiter=',', quotechar='|')
        rd = fp.read().split('\n')[1:]
        lst = []
        for row in rd:
            row = row.split()
            day, adjClose, vol = row[0], row[4], row[6]
            try:
                lst.append((str2date(day), float(adjClose), float(vol)))
            except:
                continue
        return lst


lst = loadData()
# print lst[0:10]
lst = [i for (_, i, _) in lst]
lst = list(reversed(lst))
# sys.exit()

l = len(lst)
rate = lst[-1] / lst[0]
print rate
mean = rate ** (1./l)


def diff(xs):
    return [x/y for (x, y) in zip(xs[1:], xs)]


ds = diff(lst)
# print ds


def var(xs, mean):
    t = sum([(x - mean) ** 2 for x in xs])
    return math.sqrt(t) / (len(xs) - 1)


print "period:", l
print "mean: %.4f%%" %( (mean - 1) * 100)
v = var(ds, mean)
print "var:  %.4f%%" %( v * 100)
print "range:", mean - v, mean + v

m0 = 0.0000810

print 'sharpe ratio:', (mean - 1 - m0) / v

# poerid: 246/FY
# mean: 0.0147%
# var:  0.0088%
# range: 1.000059 1.00023
# range/FY: 1.021768, 1.055116 1.087564
