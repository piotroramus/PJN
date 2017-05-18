# -*- coding: utf-8 -*-

import argparse

from preprocess_index import load_index_file


def print_context(index, entity, corpus_file):
    if entity not in index:
        print "Given entity has not been found"
    else:
        with open(corpus_file, 'rb') as corpus:
            content = corpus.read().decode('utf-8')
            for start, end, channel in index[entity]:
                print "=========================="
                print "Category:\t{}".format(channel)
                print "Coordinates:\t({},{})".format(start, end)
                print "Context: \n"
                print content[start:end + 1]


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Prints context of the given entity')
    parser.add_argument('--index_file',
                        default='resources/potop/potop_index.txt',
                        help='path to file containing indexed entities')
    parser.add_argument('--corpus_file',
                        default='resources/potop/potop_preprocessed.txt',
                        help='path to file with corpus')
    parser.add_argument('entity',
                        help='entity for which the context will be displayed')

    args = parser.parse_args()
    index_file = args.index_file
    corpus_file = args.corpus_file
    entity = args.entity

    index = load_index_file(index_file)

    print_context(index, entity, corpus_file)
