#! -*- encoding: utf8

"""python falcon.py [ledger file] [EndDate]

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
import decimal


def isInterest(item):
    return item[0] == "INTEREST"


def str2date(s):
    d = time.strptime(s, "%Y%m%d")
    d = datetime.datetime.fromtimestamp(time.mktime(d))
    return d


def loadData(fn):
    def parseLine(l):
        l = l.split()
        if len(l) != 3:
            print 'skip unknown line:', l
            return ()
        l[0] = l[0].upper()
        d = "INTEREST" if isInterest(l) else str2date(l[0])
        pjt = l[1]
        num = decimal.Decimal(l[2])
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


endDay = datetime.datetime.today()  # it return datetime class
# today = datetime.datetime.now() # it return datetime class
# today = time.time() # it return float


def calc(dat):
    """ only for one project """
    s0, s1 = 0, 0
    for (d, _, n) in dat:
        s0 += n
        s1 += (endDay - d).days * n
    return s0, s1 / decimal.Decimal(365.)


def showRatio(a, b):
    if b == 0:
        return 'N/A'
    elif a == 0:
        return '0%'
    else:
        return "%9.2f%%" % (decimal.Decimal(100.) * a / b)


if __name__ == "__main__":
    print "鸢飞戾天者，望峰息心"
    if len(sys.argv) <= 1:
        print __doc__
        sys.exit(-1)
    if len(sys.argv) == 3:
        endDay = str2date(sys.argv[2])
        print "End Day:", endDay
    else:
        print "Today:", endDay
    lst = loadData(sys.argv[1])
    # print lst
    dct, interests = splitAsPjt(lst)
    title = ("Project", "Sum0(rmb)", "Sum1(rmb*FY)",
             "INT(rmb)", "Ratio", "Ratio/FY")
    title_str = '%-20s %10s %15s %10s %10s %10s' % title
    print title_str
    bar = "-" * len(title_str)
    print bar
    fmt = "%-20s %10.2f %15.2f %10.2f %10s %10s"
    s0, s1, s2 = 0, 0, 0
    for pjt in sorted(dct.keys()):
        dat = dct[pjt]
        r = calc(dat)
        s0 += r[0]
        s1 += r[1]
        ints = interests[pjt]
        s2 += ints
        r0 = showRatio(ints, r[0])
        r1 = showRatio(ints, r[1])
        print fmt % (pjt, r[0], r[1], ints, r0, r1)
    ints = s2
    r0 = showRatio(ints, s0)
    r1 = showRatio(ints, s1)
    print bar
    print fmt % ('SUM:', s0, s1, ints, r0, r1)
    print "%-20s %10.2f" % ("FINAL:", s0 + s2)
