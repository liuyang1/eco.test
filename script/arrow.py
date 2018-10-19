"""
arrow.py [0.reporat] [1.report]
    show report on difference from 0.report to 1.report
"""
import sys
import math


def loadReport(fn):
    with open(fn) as fp:
        mainsec = False
        pjt = {}
        for l in fp.read().split('\n'):
            if l.startswith("-----"):
                mainsec = not mainsec
            elif mainsec:
                l = l.split()
                name, wcap, ints = l[0], l[2], l[3]
                pjt[name] = (float(wcap), float(ints))
        return pjt


def showPjt(pjt, dwcap, dints):
    r = dints/dwcap
    r1 = math.log(1 + r) / math.log(1 + 0.0425)
    fmt = "%-20s %10.2f %10.2f %10.2f%% %10.2f"
    print fmt % (pjt, dwcap, dints, 100 * r, r1)


f0 = sys.argv[1]
d0 = loadReport(f0)
f1 = sys.argv[2]
d1 = loadReport(f1)

swcap, sints = 0, 0
ret = {}
for pjt in d1.keys():
    wcap0, ints0 = 0, 0
    if pjt in d0.keys():
        wcap0, ints0 = d0[pjt]
    wcap1, ints1 = d1[pjt]
    dwcap = wcap1 - wcap0
    swcap += dwcap
    dints = ints1 - ints0
    sints += dints
    if dwcap == 0:
        continue
    ret[pjt] = (dwcap, dints)

for pjt in sorted(ret.keys(), key=lambda k: -ret[k][0]):
    showPjt(pjt, ret[pjt][0], ret[pjt][1])

showPjt("ALL", swcap, sints)
