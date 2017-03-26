# -*- coding: utf-8 -*-

import codecs
import matplotlib.pyplot as plt
import string
import re

from collections import Counter
from scipy.optimize import curve_fit

from plp import PLP


def mandelbrot_fit(x, B, d, P):
    return 1.0 * P / ((x + d) ** B)


def zipf_fit(x, k):
    return 1.0 * k / x


def draw_fit_plots(input_file, encoding='utf-8'):
    """ Fits functions to data and draws plots.
        This function assumes that the entries in file are already sorted in descending order."""
    data = []
    with codecs.open(input_file, 'r', encoding) as f:
        for line in f:
            _, count = line.split(',')
            data.append(int(count))

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


def draw_stats_plots(input_file, encoding='utf-8', items_num=50):
    """ Draws plots based on raw data.
        This function assumes that the entries in file are already sorted in descending order."""
    words = []
    counts = []
    with codecs.open(input_file, 'r', encoding) as f:
        for line in f:
            word, count = line.split(',')
            words.append(word)
            counts.append(int(count))

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


def generate_freq_stats(input_file, output_file, encoding='utf-8'):
    plp = PLP()
    words = Counter()
    remove_punctuation_pattern = re.compile('[%s]' % re.escape(string.punctuation))

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


if __name__ == "__main__":
    input_file = "resources/potop.txt"
    output_file = "stats.txt"

    generate_freq_stats(input_file, output_file)
    draw_stats_plots(input_file=output_file)
    draw_fit_plots(input_file=output_file)
