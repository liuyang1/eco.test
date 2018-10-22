import csv
import time
import datetime
import functools
import operator
import math


def str2date(s):
    d = time.strptime(s, "%Y-%m-%d")
    d = datetime.datetime.fromtimestamp(time.mktime(d))
    return d


def loadData():
    with open('000001.SS.csv', 'rb') as csvfile:
        rd = csv.reader(csvfile, delimiter=',', quotechar='|')
        lst = []
        for row in rd:
            day, adjClose, vol = row[0], row[5], row[6]
            try:
                lst.append((str2date(day), float(adjClose), float(vol)))
            except:
                continue
        return lst


year = 2005
begin = str2date("%d-01-01" % (year))
end = str2date("%d-01-01" % (year + 1))
lst = loadData()
lst = [p for (d, p, v) in lst if d >= begin and d <= end]
# print lst

l = len(lst)
rate = lst[-1] / lst[0]
# print rate
mean = rate ** (1./l)


def diff(xs):
    return [x/y for (x, y) in zip(xs[1:], xs)]


ds = diff(lst)
# print ds


def var(xs, mean):
    t = sum([(x - mean) ** 2 for x in xs])
    return math.sqrt(t / (len(xs) - 1))


print "poerid:", l
print "mean: %.4f%%" %( (mean - 1) * 100)
v = var(ds, mean)
print "var:  %.4f%%" %( v * 100)
print "range:", mean - v, mean + v
