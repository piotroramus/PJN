# -*- coding: utf-8 -*-

import codecs
import string
import matplotlib.pyplot as plt

import re

from collections import Counter

from plp import PLP


def draw_zipf_plots(input_file, encoding='utf-8', items_num=50):
    """ This function assumes that the entries in file are already sorted in descending order"""
    words = []
    counts = []
    with codecs.open(input_file, 'r', encoding) as f:
        for line in f:
            word, count = line.split(',')
            words.append(word)
            counts.append(int(count))

    x = range(items_num)
    plt.figure(figsize=(items_num / 6, 6))

    output = "zipf1.png"
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

    output = "zipf2.png"
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
    draw_zipf_plots(input_file=output_file)
