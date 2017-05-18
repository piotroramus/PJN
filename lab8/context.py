# -*- coding: utf-8 -*-

import argparse
import csv
from collections import defaultdict


def print_context(index, entity):
    if entity not in index:
        print "Given entity has not been found"


def load_index_file(index_file):
    index = defaultdict(list)
    with open(index_file, 'rb') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            index[row['name']].append((row['start'], row['end'], row['channel']))

    return index


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Prints context of the given entity')
    parser.add_argument('--index_file',
                        default='resources/potop/potop_index.txt',
                        help='path to file containing indexed entities')
    parser.add_argument('--corpus_file',
                        default='resources/potop/potop.txt',
                        help='path to file with corpus')
    parser.add_argument('entity',
                        help='entity for which the context will be displayed')

    args = parser.parse_args()
    index_file = args.index_file
    corpus_file = args.corpus_file
    entity = args.entity

    index = load_index_file(index_file)
    print index[entity]
