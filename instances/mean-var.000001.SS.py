# [(mean, var)]
data = [(-0.1409, 1.2341, '2018'),
        (0.0218, 0.5438, '2017'),
        (-0.0247, 1.3883, '2016'),
        (0.0225, 2.4416, '2015'),
        (0.1747, 1.0845, '2014'),
        (-0.0308, 1.1612, '2013'),
        (0.0185, 1.0959, '2012'),
        (-0.1065, 1.1533, '2011'),
        (-0.0593, 1.4198, '2010'),
        (0.2278, 1.8950, '2009'),
        (-0.4313, 2.8616, '2008'),
        (0.2737, 2.2195, '2007'),
        (0.3399, 1.3512, '2006'),
        (-0.0334, 1.3316, '2005'),
        ]

m0 = 0.0000810
# data = [(1 + y, x, year) for (y, x, year) in data]
for (r, year) in  [((mean - m0) / var, year) for (mean, var, year) in data]:
    if r > 0.048:
        print "GOOD: ", r, year
    else:
        print "BAD : ", r, year
sys.exit()
xs = [var for (_, var, _) in data]
ys = [mean for (mean, _, _) in data]


from matplotlib.pyplot import *
gca().set_xscale('log')
gca().set_yscale('log')
scatter(xs, ys)
for (y, x, txt) in data:
    # s = "%.2f %.2f %s" % (x, y, txt)
    s = txt
    annotate(s, (x, y))
grid()
# xlim(0, 3)
# ylim(-0.5, 0.5)
gca().set_aspect('equal', adjustable='box')
style.use('ggplot')
# show()
title("mean-var model for 000001.SS btw 2005-2018")
xlabel("Var/%")
ylabel("Mean/%")
savefig("1.png")
