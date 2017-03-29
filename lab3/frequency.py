# -*- coding: utf-8 -*-

import argparse
import codecs
import matplotlib.pyplot as plt
import string
import re

from collections import Counter
from scipy.optimize import curve_fit

from plp import PLP

remove_punctuation_pattern = re.compile('[%s]' % re.escape(string.punctuation))


def mandelbrot_fit(x, B, d, P):
    return 1.0 * P / ((x + d) ** B)


def zipf_fit(x, k):
    return 1.0 * k / x


def get_stats(input_file, encoding='utf-8'):
    counts = []
    words = []
    with codecs.open(input_file, 'r', encoding) as f:
        for line in f:
            word, count = line.split(',')
            counts.append(int(count))
            words.append(word)

    return counts, words


def draw_fit_plots(input_file, encoding='utf-8', **kwargs):
    """ Fits functions to data and draws plots.
        This function assumes that the entries in file are already sorted in descending order."""
    data, _ = get_stats(input_file)
    x = range(1, len(data) + 1)

    # mandelbrot fit
    initial_guess = [1.0, 0.0, 3000.0]
    (B, d, P), _ = curve_fit(mandelbrot_fit, x, data, p0=initial_guess)

    # zipf fit
    initial_guess = [1.0]
    k, _ = curve_fit(zipf_fit, x, data, p0=initial_guess)

    title = "Zipf law: f = k/x, k={}".format(round(k[0], 2))
    title += "\nMandelbrot law: f = P/((x+d)**B), P={} d={} B={}".format(round(P, 2), round(d, 2), round(B, 2))

    plt.figure(figsize=(8, 6))
    plt.title(title, fontsize=12)
    plt.plot(x, data, '-', label="Real data")
    plt.plot(x, zipf_fit(x, k), '-', label="Zipf law")
    plt.plot(x, mandelbrot_fit(x, B, d, P), '-', label="Mandelbrot law")
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.yscale('log')
    plt.ylim(ymin=0.1)
    plt.legend()
    plt.savefig("zipf_mandelbrot.png")


def draw_raw_plots(input_file, encoding='utf-8', items_num=50, **kwargs):
    """ Draws plots based on raw data.
        This function assumes that the entries in file are already sorted in descending order."""
    counts, words = get_stats(input_file)

    x = range(items_num)
    plt.figure(figsize=(items_num / 6, 6))

    output = "zipf_stat.png"
    plt.title("Zipf law for the Potop book")
    plt.plot(x, counts[:items_num])
    plt.xticks(x, words[:items_num], rotation=90)
    plt.tight_layout()
    plt.savefig(output)
    plt.gcf().clear()

    cumulative_y = []
    all_sum = float(sum(counts))
    current_sum = 0
    for i in xrange(items_num):
        current_sum += counts[i]
        cumulative_y.append((current_sum / all_sum) * 100)

    output = "zipf_stat_cumulative.png"
    plt.title("Cumulative Zipf law for the Potop book")
    plt.plot(x, cumulative_y)
    plt.xticks(x, words[:items_num], rotation=90)
    plt.tight_layout()
    plt.savefig(output)


def generate_freq_stats(input_file, output_file, encoding='utf-8', **kwargs):
    plp = PLP()
    words = Counter()

    with codecs.open("out.txt", 'w', encoding) as out:
        with codecs.open(input_file, 'r', encoding) as f:
            for line in f:

                line = remove_punctuation_pattern.sub('', line.lower())

                for word in line.split():

                    ids = plp.rec(word)
                    if not ids:
                        words[word] += 1
                    for i in ids:
                        basic = plp.bform(i)
                        words[basic] += 1
                        # take basic form and ignore other because syntactically they are the same
                        break

    with codecs.open(output_file, 'w', encoding) as f:
        for word, count in words.most_common(len(words)):
            f.write(word + "," + str(count) + "\n")


def quantitive_count(input_file, encoding='utf-8', **kwargs):
    """ Counts hapax legomena and words which make 50% of the text"""
    data, _ = get_stats(input_file, encoding)

    hapax_legomena = data.count(1)
    print "Hapax legomena: {}".format(hapax_legomena)

    half_of_all = 1.0 * sum(data) / 2
    words_making_half_text = 0
    current_sum = 0
    for e in data:
        current_sum += e
        words_making_half_text += 1
        if current_sum >= half_of_all:
            break

    print "Number of words which make 50% of the text: {}".format(words_making_half_text)


def word_ngrams(n, words):
    """ Counts word-level ngrams"""
    ngrams = Counter()

    l = len(words)
    for i in xrange(l - n):
        ngram = " ".join(words[i:i + n])
        ngrams[ngram] += 1

    return ngrams


def determine_ngrams(input_file, encoding='utf-8', **kwargs):
    """ Find word-based di-grams and tri-grams for the text in input file"""

    for n in [2, 3]:
        with codecs.open(input_file, 'r', encoding) as f:
            data = f.read().strip().lower()

            # remove digits, interpunction and other strange characters
            data = remove_punctuation_pattern.sub('', data)

            data = data.split()
            ngrams = word_ngrams(n, data)
            with codecs.open("{}-ngrams.txt".format(n), 'w', encoding) as out:
                for ngram, count in ngrams.most_common(len(ngrams)):
                    out.write(ngram + ": " + str(count) + "\n")


if __name__ == "__main__":
    input_file = "resources/potop.txt"
    output_file = "stats.txt"

    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['rank', 'raw_plots', 'fit_plots', 'hl', 'ngrams'],
                        help='action to be taken')
    parser.add_argument('--input_file',
                        help='path to file with input data')
    parser.add_argument('--output_file',
                        help='output file for the rank action')

    args = parser.parse_args()

    action = args.action
    input_file = args.input_file
    output_file = args.output_file

    actions = {
        'rank': generate_freq_stats,
        'raw_plots': draw_raw_plots,
        'fit_plots': draw_fit_plots,
        'hl': quantitive_count,
        'ngrams': determine_ngrams,
    }

    actions[action](input_file=input_file, output_file=output_file)
