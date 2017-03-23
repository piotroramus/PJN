# -*- coding: utf-8 -*-

import codecs
import string
import re
from collections import Counter

from plp import PLP


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
