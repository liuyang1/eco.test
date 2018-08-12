"""
Yuan Fei Li Tian Zhe, Wang Feng Xi Xin;

python falcon.py [ledger file]

ledger file format:

    YYYYMMDD    PROJECT_NAME    [+-]NUMBER

It will show result:

    PROJECT_NAME    FINAL_NUMBER    NUMBERxDAY

It will help to calculate interest in investment.

ratio = Interest / SUM1
"""

import sys
import time
import datetime


def loadData(fn):
    def parseLine(l):
        l = l.split()
        if len(l) != 3:
            print 'skip unknown line:', l
            return ()
        # d = l[0]
        d = time.strptime(l[0], '%Y%m%d')
        d = datetime.datetime.fromtimestamp(time.mktime(d))
        pjt = l[1]
        # num = l[2]
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
    dct = {}
    for pjt in pjts:
        dct[pjt] = [i for i in dat if i[1] == pjt]
    return dct


today = datetime.datetime.today()  # it return datetime class
# today = datetime.datetime.now() # it return datetime class
# today = time.time() # it return float


def calc(dat):
    """ only for one project """
    s0, s1 = 0, 0
    for (d, _, n) in dat:
        s0 += n
        s1 += (today - d).days * n
    return s0, s1


if __name__ == "__main__":
    print "Now:", today
    lst = loadData(sys.argv[1])
    # print lst
    dct = splitAsPjt(lst)
    print '%-20s %10s %20s %20s' % ("PROJECT_NAME", "SUM0/rmb", "SUM1/(rmb*day)", "SUM1(/rmb*year)")
    s0, s1 = 0, 0
    for pjt, dat in dct.items():
        r = calc(dat)
        s0 += r[0]
        s1 += r[1]
        print "%-20s %10.2f %20.2f %20.2f" % (pjt, r[0], r[1], r[1]/365.)
    print "%-20s %10.2f %20.2f %20.2f" % ('sum', s0, s1, s1/365.)
