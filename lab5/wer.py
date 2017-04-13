def levenshtein_distance(s1, s2):
    n, m = len(s1), len(s2)
    if n == 0:
        return m
    if m == 0:
        return n
    matrix = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]
    for i in xrange(m + 1):
        matrix[i][0] = i
    for i in xrange(n + 1):
        matrix[0][i] = i

    for i, c1 in enumerate(s1):
        for j, c2 in enumerate(s2):
            cost = int(c1 != c2)
            matrix[j + 1][i + 1] = min(matrix[j][i + 1] + 1, matrix[j + 1][i] + 1, matrix[j][i] + cost)

    return matrix[m][n]


def word_error_rate(reference, hypothesis):
    ref = reference.lower().split()
    hyp = hypothesis.lower().split()
    return levenshtein_distance(ref, hyp)
