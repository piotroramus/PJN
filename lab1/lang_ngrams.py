import codecs
import glob
import os
import re
import sys

from collections import Counter
from unidecode import unidecode

from corpus_definitions import get_corpuses, languages_set


def build_lang_statistics(n, lang, corpus_results_dir, lang_results_dir):
    # filenaming convention is prefix_lang_n.txt
    pattern = "*_{}_{}.txt".format(lang, n)

    result = Counter()
    for fn in glob.glob(os.path.join(corpus_results_dir, pattern)):
        with open(fn, 'r') as f:
            for line in f:
                ngram, count = line.split(' ')
                result[ngram] += int(count)

    output_file = os.path.join(lang_results_dir, "{}_{}.txt".format(lang, n))
    save_results(output_file, result)


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
        print "Building {}-grams for {}...".format(n, corpus['filename'])
        with codecs.open(corpus['filename'], 'r', corpus.get('charset', 'utf-8')) as fn:
            stat = determine_ngrams(fn.read(), n)
            filename_without_extension = corpus['filename'].split('/')[-1].split('.')[0]
            output_file = os.path.join(results_dir,
                                       "{}_{}_{}.txt".format(filename_without_extension, corpus['lang'], n))
            save_results(output_file, stat)


def save_results(filename, dictionary):
    with open(filename, 'w') as fn:
        for key in dictionary:
            fn.write("{} {}\n".format(key, dictionary[key]))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Program usage: %s n".format(sys.argv[0])
        sys.exit(1)

    n = int(sys.argv[1])

    corpus_results_dir = os.path.join("results", "corpus")
    lang_results_dir = os.path.join("results", "lang")

    generate_statistics(n, corpus_results_dir)

    available_languages = languages_set()
    for lang in available_languages:
        print "Gathering statistics for {} language...".format(lang)
        build_lang_statistics(n, lang, corpus_results_dir, lang_results_dir)
