import io
import re
import string

from collections import Counter


def create_stoplist(input_file, output_file='resources/stoplist.txt', encoding='utf-8', most_common=20):
    """ Creates stoplist based on word frequency"""

    from utils import basic_form

    remove_punctuation_pattern = re.compile('[%s]' % re.escape(string.punctuation))

    words = Counter()
    with io.open(input_file, 'r', encoding=encoding) as f:
        content = f.read()
        content = remove_punctuation_pattern.sub(' ', content).lower()

        for word in content.strip().split():
            bword = basic_form(word)
            words[bword] += 1

    with io.open(output_file, 'w', encoding=encoding) as f:
        for word, _ in words.most_common(most_common):
            f.write(word)
            f.write(u'\n')


def load_stoplist(stoplist_file='resources/stoplist.txt', encoding='utf-8'):
    """ Loads already created stoplist from file """
    stoplist = list()
    with io.open(stoplist_file, 'r', encoding=encoding) as f:
        for line in f:
            stoplist.append(line.strip())
    return stoplist


def apply_stoplist_to_doc(stoplist, document):
    filtered_document = list()
    for word in document:
        if word not in stoplist:
            filtered_document.append(word)
    return filtered_document
