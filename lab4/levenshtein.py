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

others = {
    u'z': [u's', u'ś'],
    u'i': [u'j'],
    u'u': [u'ł', u'ó'],
    u'k': [u'g'],
    u'w': [u'f'],
    u'p': [u'b'],
    u'd': [u't'],
    u'o': [u'ą'],
}

OTHER_ERRORS_COST = 0.25
DIACRITICS_COST = 0.25
CZECH_ERROR_COST = 0.5


def equal_to_special_char(c1, c2, special_characters):
    if c1 == c2:
        return True
    if c1 in special_characters:
        for d in special_characters[c1]:
            if c2 == d:
                return True
    if c2 in special_characters:
        for d in special_characters[c2]:
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
            elif equal_to_special_char(c1, c2, diacritics):
                cost_matrix[j][i] = DIACRITICS_COST
            elif equal_to_special_char(c1, c2, others):
                cost_matrix[j][i] = OTHER_ERRORS_COST
            if i > 1 and j > 1 and word1[i - 1] == c2 and word2[j - 1] == c1:
                cost_matrix[j - 1][i - 1] = 1
                cost_matrix[j][i] = CZECH_ERROR_COST - 1

            metric_matrix[j + 1][i + 1] = min(metric_matrix[j][i + 1] + 1, metric_matrix[j + 1][i] + 1,
                                              metric_matrix[j][i] + cost_matrix[j][i])

    return metric_matrix[m][n]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('word1', help='first word to compare')
    parser.add_argument('word2', help='second word to compare')
    parser.add_argument('-p', '--print_result', help='print the result', action='store_true')
    args = parser.parse_args()

    word1 = unicode(args.word1, 'utf-8')
    word2 = unicode(args.word2, 'utf-8')
    print_result = args.print_result

    dist = modified_levenshtein_distance(word1, word2)

    if print_result:
        print "Levenshtein distance from " + word1 + " to " + word2 + ": " + str(dist)
