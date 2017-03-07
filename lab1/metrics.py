from math import fsum, sqrt


def normalize(vec):
    s = fsum(vec.values())
    normalized_v0 = {k: v / s for k, v in vec.items()}
    return normalized_v0


def vlen(v):
    return sqrt(fsum(v ** 2 for v in v.values()))


def euclidean_metric(v1, v2):
    keys = set(v1.keys()) | set(v2.keys())
    sum = 0
    for key in keys:
        sum += (v1.get(key, 0) - v2.get(key, 0)) ** 2
    return sqrt(sum)


def taxi_metric(v1, v2):
    keys = set(v1.keys()) | set(v2.keys())
    sum = 0
    for key in keys:
        sum += abs(v1.get(key, 0) - v2.get(key, 0))
    return sum


def max_metric(v1, v2):
    keys = set(v1.keys()) | set(v2.keys())
    sum = 0
    for key in keys:
        sum = max(sum, abs(v1.get(key, 0) - v2.get(key, 0)))
    return sum


def cosine_metric(v1, v2):
    keys = set(v1.keys()) | set(v2.keys())
    sum = 0
    for key in keys:
        sum += v1.get(key, 0) * v2.get(key, 0)
    return 1 - (sum/float(vlen(v1)*vlen(v2)))