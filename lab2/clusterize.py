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


def longest_common_subsequence_length(s1, s2):
    """ Length of the longest common subsequence of strings s1 and s2"""
    n, m = len(s1), len(s2)
    c = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]

    for i, c1 in enumerate(s1):
        for j, c2 in enumerate(s2):
            if c1 == c2:
                c[j + 1][i + 1] = c[j][i] + 1
            elif c[j + 1][i] >= c[j][i + 1]:
                c[j + 1][i + 1] = c[j + 1][i]
            else:
                c[j + 1][i + 1] = c[j][i + 1]

    return c[m][n]


def longest_common_substring_length(s1, s2):
    """ Length of the longest common substring of strings s1 and s2"""
    n, m = len(s1), len(s2)
    c = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]

    longest = 0
    for i, c1 in enumerate(s1):
        for j, c2 in enumerate(s2):
            if c1 == c2:
                c[j + 1][i + 1] = c[j][i] + 1
                if c[j + 1][i + 1] > longest:
                    longest = c[j + 1][i + 1]
            else:
                c[j + 1][i + 1] = 0

    return longest


def levenshtein_metric(s1, s2):
    """ Normalized distance between strings s1 and s2 where
        0 == perfect match
        1 == completely different strings
        based on the Levenshtein distance between s1 and s2
    """
    return levenshtein_distance(s1, s2) / float(max(len(s1), len(s2)))


def longest_common_subsequence_metric(s1, s2):
    """ Normalized distance between strings s1 and s2 where
        0 == perfect match
        1 == completely different strings
        based on the length of the longest common subsequence of s1 and s2
    """
    return 1 - longest_common_subsequence_length(s1, s2) / float(max(len(s1), len(s2)))


def longest_common_substring_metric(s1, s2):
    """ Normalized distance between strings s1 and s2 where
        0 == perfect match
        1 == completely different strings
        based on the length of the longest common substring of s1 and s2
    """
    return 1 - longest_common_substring_length(s1, s2) / float(max(len(s1), len(s2)))
