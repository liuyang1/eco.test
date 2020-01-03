tbl = [(5, 4.262), (4.75, 4.241), (4.5, 4.219), (4.25, 4.196),
        (4, 4.171), (3.75, 4.144), (3.5, 4.115), (3.25, 4.084), (3, 4.05)]


def diff(t, r):
    ds = [(abs(t - t_), r - r_) for t_, r_ in tbl]
    ro = sorted(ds)[0]
    return ro


def best(xs):
    rs = [diff(a, b) for a, b in xs]
    print rs
    b = sorted(rs, key=lambda x: -x[1])
    return b[0]


xs = [(3.5, 4.18),
        (4+2/12, 4.24)]
print(best(xs))
