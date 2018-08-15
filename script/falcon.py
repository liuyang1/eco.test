#! -*- encoding: utf8

"""鸢飞戾天者，望峰息心

python falcon.py [ledger file]

ledger file format:

    YYYYMMDD    PROJECT_NAME    [+-]NUMBER
    日期        项目名称        流入流出金额

It will show result:

    PROJECT_NAME    FINAL_NUMBER    NUMBER*YEAR
    项目名称        当前累计金额    元*年

It will help to calculate interest in investment.
    ratio = Interest / SUM1

在频繁操作的情况下，这个脚本帮助计算自己的年化收益
    年化收益 = 收益 / 元年
"""

import sys
import time
import datetime


def isInterest(item):
    return item[0] == "INTEREST"


def loadData(fn):
    def parseLine(l):
        l = l.split()
        if len(l) != 3:
            print 'skip unknown line:', l
            return ()
        l[0] = l[0].upper()
        if isInterest(l):
            d = "INTEREST"
        else:
            d = time.strptime(l[0], '%Y%m%d')
            d = datetime.datetime.fromtimestamp(time.mktime(d))
        pjt = l[1]
        num = float(l[2])
        return (d, pjt, num)
    lst = []
    with open(fn) as f:
        for l in f.read().split('\n'):
            l = l.strip()
            if len(l) == 0 or l[0] == '#':
                continue
            tp = parseLine(l)
            lst.append(tp)
    return lst


def splitAsPjt(dat):
    pjts = set([i[1] for i in dat])
    dct, interests = {}, {}
    for pjt in pjts:
        pjtdata = [i for i in dat if i[1] == pjt]
        dct[pjt] = [i for i in pjtdata if not isInterest(i)]
        interests[pjt] = sum([i[2] for i in pjtdata if isInterest(i)])
    return dct, interests


today = datetime.datetime.today()  # it return datetime class
# today = datetime.datetime.now() # it return datetime class
# today = time.time() # it return float


def calc(dat):
    """ only for one project """
    s0, s1 = 0, 0
    for (d, _, n) in dat:
        s0 += n
        s1 += (today - d).days * n
    return s0, s1 / 365.


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print __doc__
        sys.exit(-1)
    print "End Day:", today
    lst = loadData(sys.argv[1])
    # print lst
    dct, interests = splitAsPjt(lst)
    title = ("Project", "Sum0(rmb)", "Sum1(rmb*FY)",
             "Interest(rmb)", "Ratio(%)", "Ratio/FY(%)")
    print '%-20s %10s %20s %20s %10s %10s' % title
    s0, s1, s2 = 0, 0, 0
    for pjt, dat in dct.items():
        r = calc(dat)
        s0 += r[0]
        s1 += r[1]
        ints = interests[pjt]
        s2 += ints
        if r[0] == 0:
            ratio0 = float('NaN')
        else:
            ratio0 = 100. * ints / r[0]
        ratio1 = 100. * ints / r[1]
        print "%-20s %10.2f %20.2f %20.2f %10.2f %10.2f" % (pjt, r[0], r[1], ints, ratio0, ratio1)
    print "%-20s %10.2f %20.2f %20.2f %10.2f %10.2f" % ('SUM', s0, s1, s2, 100 * s2 / s0, 100 * s2 / s1)
