from math import fsum, sqrt


def vlen(v):
    return sqrt(fsum(v ** 2 for v in v.values()))


def normalize(vec):
    l = vlen(vec)
    normalized_v0 = {k: v / l for k, v in vec.items()}
    return normalized_v0


def euclidean_metric(v1, v2):
    keys = set(v1.keys()) | set(v2.keys())
    s = 0
    for key in keys:
        s += (v1.get(key, 0) - v2.get(key, 0)) ** 2
    return sqrt(s)


def taxi_metric(v1, v2):
    keys = set(v1.keys()) | set(v2.keys())
    s = 0
    for key in keys:
        s += abs(v1.get(key, 0) - v2.get(key, 0))
    return s


def max_metric(v1, v2):
    keys = set(v1.keys()) | set(v2.keys())
    s = 0
    for key in keys:
        s = max(s, abs(v1.get(key, 0) - v2.get(key, 0)))
    return s


def cosine_metric(v1, v2):
    keys = set(v1.keys()) | set(v2.keys())
    s = 0
    for key in keys:
        s += v1.get(key, 0) * v2.get(key, 0)
    # omitting float(vlen(v1)*vlen(v2)) since it is equal to 1
    return 1 - s
