import codecs
import re

from pprint import pprint
from unidecode import unidecode


def load_stoplist():
    # words from specified lists will be merged
    # this is to cope with multi-language data
    stoplists = [
        'stoplists/stoplist_en.txt',
        'stoplists/stoplist_pl.txt'
    ]

    stoplist = set()

    for sl in stoplists:
        with codecs.open(sl, 'r', 'utf-8') as f:
            for line in f:

                if line.startswith("#"):
                    continue

                line = unidecode(line.strip().lower())
                stoplist.add(line)

    return stoplist


def apply_stoplist(data):
    pass


def preprocess(line):
    only_letters_and_digits = re.compile("[^a-z0-9\s]")
    multiple_whitespaces = re.compile('\s+')

    line = unidecode(line.strip().lower())
    line = only_letters_and_digits.sub(' ', line)
    line = multiple_whitespaces.sub(' ', line.strip())

    return line


def clusterize():
    input_file = "resources/lines.txt"

    output_file = 'preprocessed.txt'

    with open(output_file, 'w') as outf:
        with codecs.open(input_file, 'r', 'utf-8') as f:
            for line in f:
                line = preprocess(line)
                outf.write("{}\n".format(line))


if __name__ == '__main__':
    clusterize()
