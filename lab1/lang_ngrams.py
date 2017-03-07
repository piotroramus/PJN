import codecs
import os
import re
import sys

from collections import Counter
from unidecode import unidecode

from corpus_definitions import get_corpuses


def determine_ngrams(data, n):
    ngrams = Counter()

    data = unidecode(data.lower())

    # remove digits, interpunction and other strange characters
    not_letters = re.compile("[^a-z\s]")
    data = not_letters.sub('', data)

    for word in data.split():
        # the idea is to create n lists of characters
        # every next list "loses" its first element
        # then the lists are zipped creating ngrams
        for ngram in zip(*(word[c:] for c in range(n))):
            key = "".join(ngram)
            ngrams[key] += 1
    return ngrams


def generate_statistics(n, results_dir):
    for corpus in get_corpuses():
        print "Processing corpus {}...".format(corpus['filename'])
        with codecs.open(corpus['filename'], 'r', corpus.get('charset', 'utf-8')) as fn:
            stat = determine_ngrams(fn.read(), n)
            print stat
            filename_without_extension = corpus['filename'].split('/')[-1].split('.')[0]
            output_file = os.path.join(results_dir, "{}_{}.txt".format(filename_without_extension, n))
            save_results(output_file, stat)


def save_results(filename, result):
    with open(filename, 'w') as fn:
        for ngram in result:
            fn.write("{} {}\n".format(ngram, result[ngram]))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Program usage: %s n".format(sys.argv[0])
        sys.exit(1)

    n = int(sys.argv[1])

    results_dir = "results"

    generate_statistics(n, results_dir)
