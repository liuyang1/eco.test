"""
arrow.py [0.reporat] [1.report]
    show report on difference from 0.report to 1.report
"""
import sys
import math
import time
import datetime


def str2date(s):
    l = len("2018-01-01")
    s = s[0:l]
    d = time.strptime(s, "%Y-%m-%d")
    d = datetime.datetime.fromtimestamp(time.mktime(d))
    return d


def loadReport(fn):
    with open(fn) as fp:
        mainsec = False
        pjt = {}
        dayKey = ["End Day: ", "Today: "]
        for l in fp.read().split('\n'):
            if any([l.startswith(i) for i in dayKey]):
                for key in dayKey:
                    try:
                        d = l.index(key) + len(key)
                    except ValueError:
                        continue
                    day = str2date(l[d:])
            elif l.startswith("-----"):
                mainsec = not mainsec
            elif mainsec:
                l = l.split()
                name, wcap, ints = l[0], l[2], l[3]
                pjt[name] = (float(wcap), float(ints))
        return day, pjt


def showTitle():
    fmt = "%-20s %10s %10s %10s %10s"
    return fmt % ("Project", "WCap/$*FY", "Int/$", "MDietz", "LogMDietz/B")


def showPjt(pjt, dwcap, dints):
    r = dints/dwcap
    r1 = math.log(1 + r) / math.log(1 + 0.0425)
    fmt = "%-20s %10.2f %10.2f %10.2f%% %10.2f"
    return fmt % (pjt, dwcap, dints, 100 * r, r1)


def showBar(title):
    return '-' * len(title)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print __doc__
        sys.exit()

    day0, d0 = loadReport(sys.argv[1])
    day1, d1 = loadReport(sys.argv[2])

    ret = {}
    for pjt in d1.keys():
        wcap0, ints0 = 0, 0
        if pjt in d0.keys():
            wcap0, ints0 = d0[pjt]
        wcap1, ints1 = d1[pjt]
        dwcap = wcap1 - wcap0
        dints = ints1 - ints0
        if dwcap == 0:
            continue
        ret[pjt] = (dwcap, dints)

    swcap = sum([i[0] for i in ret.values()])
    sints = sum([i[1] for i in ret.values()])

    title = showTitle()
    bar = showBar(title)

    # display report
    print "from: ", day0
    print "end:  ", day1
    print title
    print bar
    for pjt in sorted(ret.keys(), key=lambda k: -ret[k][0]):
        print showPjt(pjt, ret[pjt][0], ret[pjt][1])
    print bar
    print showPjt("ALL", swcap, sints)
