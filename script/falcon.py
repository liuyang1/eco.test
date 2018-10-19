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
import itertools
import math
import scipy.optimize

D365 = 365.
endDay = datetime.datetime.today()  # it return datetime class
baseRate = 0.0425
# today = datetime.datetime.now() # it return datetime class
# today = time.time() # it return float


def isInterest(item):
    return item[0] == "INTEREST"


def str2date(s):
    d = time.strptime(s, "%Y%m%d")
    d = datetime.datetime.fromtimestamp(time.mktime(d))
    return d


def linearBaseRate(r):
    return math.log(1 + r) / math.log(1 + baseRate)


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


def calc(pjt, cf, ints):
    """ only for one project
        input : [(date, project, number)], ints
        output : captital, captital * dT, interest, ratio * dT, IRR, cf
    """
    s0 = sum([n for (_, n) in cf])
    s1 = sum([n * (endDay - d).days / D365 for (d, n) in cf])
    if abs(s0) >= 0.001:
        te = endDay
        cf.append((te, -(s0 + ints)))
    else:
        te = max([d for (d, _) in cf])
        cf.append((te, -ints))
    return pjt, s0, s1, ints, cf


def showRatio(a, b=1):
    if b == 0:
        return 'N/A'
    elif a == 0:
        return '0%'
    else:
        return "%9.2f%%" % (100 * a / b)


def showTitle():
    title = ("Project", "Cap/$", "WCap/$*FY",
             "Int/$", "HPR", "MDietz", "IRR", "LogMDietz/B")
    return '%-20s %10s %10s %10s %10s %10s %10s %10s' % title


def showBar(title):
    return '-' * len(title)


def showPjt(pjt):
    name, s0, s1, ints, cf = pjt
    r0 = showRatio(ints, s0)
    r1 = ints / s1
    r2 = showRatio(xirr(cf))
    r3 = linearBaseRate(r1)
    r1 = showRatio(r1)
    fmt = "%-20s %10.2f %10.2f %10.2f %10s %10s %10s %10.2f"
    return fmt % (name, s0, s1, ints, r0, r1, r2, r3)


if __name__ == "__main__":
    print "鸢飞戾天者，望峰息心"  # slogan
    if len(sys.argv) <= 1:
        print __doc__
        sys.exit(-1)
    if len(sys.argv) == 3:
        endDay = str2date(sys.argv[2])
        print "End Day:", endDay
    else:
        print "Today:", endDay
    lst = loadData(sys.argv[1])
    dct, ints = splitAsPjt(lst)
    result = []
    for pjt in dct.keys():
        result.append(calc(pjt, dct[pjt], ints[pjt]))
    ss0 = sum([i[1] for i in result])
    ss1 = sum([i[2] for i in result])
    sints = sum([i[3] for i in result])
    scf = list(itertools.chain(*[i[4] for i in result]))  # concat
    final = ("ALL", ss0, ss1, sints, scf)

    title = showTitle()
    bar = showBar(title)

    print "Target Rate: %s" % (showRatio(baseRate))
    print title
    print bar
    # sorted with (SUM, SUM*dT), but instead of project's NAME
    for pjt in sorted(result, key=lambda k: (-k[1], -k[2])):
        print showPjt(pjt)
    print bar
    print showPjt(final)
    print "%-20s %10.2f" % ("FINAL", ss0 + sints)
