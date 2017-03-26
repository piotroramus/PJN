# coding=utf-8

import argparse

diacritics = {
    u'a': [u'ą'],
    u'c': [u'ć'],
    u'e': [u'ę'],
    u'l': [u'ł'],
    u'n': [u'ń'],
    u'o': [u'ó'],
    u's': [u'ś'],
    u'z': [u'ż', u'ź'],
}

DIACRITICS_COST = 0.25
CZECH_ERROR_COST = 0.5


def equal_to_diactiricts(c1, c2):
    if c1 == c2:
        return True
    if c1 in diacritics:
        for d in diacritics[c1]:
            if c2 == d:
                return True
    if c2 in diacritics:
        for d in diacritics[c2]:
            if c1 == d:
                return True
    return False


def modified_levenshtein_distance(word1, word2):
    n, m = len(word1), len(word2)
    if n == 0:
        return m
    if m == 0:
        return n

    metric_matrix = [[0 for _ in xrange(n + 1)] for _ in xrange(m + 1)]
    cost_matrix = [[1 for _ in xrange(n + 1)] for _ in xrange(m + 1)]

    for i in xrange(m + 1):
        metric_matrix[i][0] = i
    for i in xrange(n + 1):
        metric_matrix[0][i] = i

    for i, c1 in enumerate(word1):
        for j, c2 in enumerate(word2):

            if c1 == c2 and cost_matrix[j][i] == 1:
                # the words are equal, so we do not want to add anything
                cost_matrix[j][i] = 0
            elif equal_to_diactiricts(c1, c2):
                cost_matrix[j][i] = DIACRITICS_COST
            if i > 1 and j > 1 and word1[i - 1] == c2 and word2[j - 1] == c1:
                cost_matrix[j - 1][i - 1] = 1
                cost_matrix[j][i] = CZECH_ERROR_COST - 1

            metric_matrix[j + 1][i + 1] = min(metric_matrix[j][i + 1] + 1, metric_matrix[j + 1][i] + 1,
                                              metric_matrix[j][i] + cost_matrix[j][i])

    for e in metric_matrix:
        print e
    print
    for e in cost_matrix:
        print e

    return metric_matrix[m][n]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('word1', help='first word to compare')
    parser.add_argument('word2', help='second word to compare')
    args = parser.parse_args()

    word1 = unicode(args.word1, 'utf-8')
    word2 = unicode(args.word2, 'utf-8')

    dist = modified_levenshtein_distance(word1, word2)
    print "Levenshtein distance from " + word1 + " to " + word2 + ": " + str(dist)
