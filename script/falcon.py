#! -*- encoding: utf8

"""python falcon.py [ledger file] [EndDate]

ledger file format:

    YYYYMMDD    PROJECT_NAME    [+-]NUMBER
    日期        项目名称        流入流出金额

Recoding interest by this format

    Interest    PROJECT_NAME    [+-]NUMBER
    利息标记    项目名称        利息

This is sample of ledger file:
以下是账本文件的样例
    20180101        ABC             1000
    20180102        ABC             -1000
    Interest        ABC             1.0
    20180201        XYZ             1000

It will show result:

    PROJECT_NAME    FINAL_NUMBER    NUMBER*YEAR
    项目名称        当前累计金额    元*年

It will help to calculate IRR(Internal Rate of Return) in investment.
"""

import sys
import time
import datetime
import scipy.optimize

D365 = 365.
endDay = datetime.datetime.today()  # it return datetime class
# today = datetime.datetime.now() # it return datetime class
# today = time.time() # it return float


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


def xnpv(rate, cashflows):
    t0 = min([d for (d, _) in cashflows])
    return sum([cf / (1 + rate) ** ((t - t0).days / D365) for (t, cf) in cashflows])


def xirr(cashflows):
    return scipy.optimize.newton(lambda r: xnpv(r, cashflows), 0.0001)


def splitAsPjt(dat):
    pjts = set([i[1] for i in dat])
    dct, ints = {}, {}
    for pjt in pjts:
        pjtdata = [i for i in dat if i[1] == pjt]
        dct[pjt] = [(i[0], i[2]) for i in pjtdata if not isInterest(i)]
        ints[pjt] = sum([i[2] for i in pjtdata if isInterest(i)])
    return dct, ints


def calc(dat, ints):
    """ only for one project
        input : [(date, project, number)], ints
        output : captital, captital * dT, interest, ratio * dT, IRR, cf
    """
    s0 = sum([n for (_, n) in dat])
    s1 = sum([n * (endDay - d).days / D365 for (d, n) in dat])
    if abs(s0) >= 0.001:
        te = endDay
        dat.append((te, -(s0 + ints)))
    else:
        te = max([d for (d, _) in dat])
        dat.append((te, -ints))
    cf = dat
    r1 = ints / s1
    r2 = xirr(cf)
    return s0, s1, ints, r1, r2, cf


def showRatio(a, b=1):
    if b == 0:
        return 'N/A'
    elif a == 0:
        return '0%'
    else:
        return "%9.2f%%" % (100 * a / b)


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
    title = ("Project", "Sum0(rmb)", "Sum1(rmb*FY)",
             "INT(rmb)", "Ratio", "Ratio/FY", "IRR")
    title_str = '%-20s %10s %15s %10s %10s %10s %10s' % title
    print title_str
    bar = "-" * len(title_str)
    print bar
    fmt = "%-20s %10.2f %15.2f %10.2f %10s %10s %10s"
    dct, ints = splitAsPjt(lst)
    result, sum_cf = [], []
    sum0, sum1, sum_int = 0, 0, 0
    for pjt in dct.keys():
        r = calc(dct[pjt], ints[pjt])
        s0, s1, s2, r1, r2, cf = r
        r0 = showRatio(s2, s0)
        r1 = showRatio(r1)
        r2 = showRatio(r2)
        result.append((pjt, s0, s1, s2, r0, r1, r2))
        sum0 += s0
        sum1 += s1
        sum_int += s2
        sum_cf.extend(cf)
    # sorted with (SUM, SUM*dT), but instead of project's NAME
    for pjt in sorted(result, key=lambda k: (-k[1], -k[2])):
        print fmt % pjt
    r0 = showRatio(sum_int, sum0)
    r1 = showRatio(sum_int, sum1)
    r2 = showRatio(xirr(sum_cf))
    print bar
    print fmt % ('SUM:', sum0, sum1, sum_int, r0, r1, r2)
    print "%-20s %10.2f" % ("FINAL:", sum0 + sum_int)
