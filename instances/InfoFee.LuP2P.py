"""
LuP2P 0.07%% information fee

This is charged per every month, and based on payment.

"""

import numpy


def acc(xs):
    y = 0
    for x in xs:
        y += x
        yield y


pv = 50000
nper = 12 * 3


def infoFee(rate):
    xs = numpy.ppmt(0.084 / 12, range(nper), nper, -pv)
    # print xs
    bases = acc(xs)
    # print bases
    fees = [(pv - a) * rate for a in bases]
    # print fees
    fee = sum(fees)
    return fee

rate = 0.07 * 0.01

def calc(rate):
    f = infoFee(rate)
    print f, "%.2f%%" % (f / pv * 100.)

calc(rate)
# 643.14 1.29%
calc(rate * 0.5)
# 321.57 0.64%
calc(rate * 0.3)
# 192.94 0.39%
