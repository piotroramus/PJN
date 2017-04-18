def cosine_metric(v1, v2):
    keys = set(v1.keys()) & set(v2.keys())
    s = 0
    for key in keys:
        s += v1.get(key, 0) * v2.get(key, 0)
    return 1 - s
