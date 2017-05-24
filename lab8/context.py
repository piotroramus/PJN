# -*- coding: utf-8 -*-

import argparse

from mapping import load_mapping, get_original_positions
from preprocess_index import load_index_file


def print_context(index, entity, corpus_file, mapping, context_size):
    if entity not in index:
        print 'Entity "{}" has not been found'.format(entity)
    else:
        with open(corpus_file, 'rb') as corpus:
            content = corpus.read().decode('utf-8')
            for start, end, channel in index[entity]:
                print "================================="
                print "Category:\t{}".format(channel)
                print "Position:\t({},{})".format(start, end)

                # hack: for "complex" entity like "Jasna Gora" move end to the first whitespace
                if " " in entity:
                    end -= (len(entity) - entity.index(" "))

                start, end = get_original_positions(mapping, start, end)

                # find context_size lines preceding and following the entity to show the entity's context
                # search backwards
                found_lines = 0
                current_index = start - 1
                while current_index > 0 and found_lines < context_size:
                    if content[current_index] != '\n':
                        current_index -= 1
                        continue
                    found_lines += 1
                    current_index -= 1
                context_start = current_index

                # look forward
                found_lines = 0
                current_index = end + 1
                max_index = len(content)
                while current_index < max_index and found_lines < context_size:
                    if content[current_index] != '\n':
                        current_index += 1
                        continue
                    found_lines += 1
                    current_index += 1
                context_end = current_index

                print "In corpus:\t({},{})".format(start, end)
                print "Context: \n"
                print content[context_start:context_end]


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Prints context of the given entity')
    parser.add_argument('--index_file',
                        default='resources/potop/potop_index.txt',
                        help='path to file containing indexed entities')
    parser.add_argument('--corpus_file',
                        default='resources/potop/potop.txt',
                        help='path to file with corpus')
    parser.add_argument('--mapping_file',
                        default='resources/potop/stripped_original_mapping.txt',
                        help='path to containing mapping between stripped corpus and original version')
    parser.add_argument('-s', '--context_size',
                        type=int,
                        default=5,
                        help='number of lines to show the entity context')
    parser.add_argument('entity',
                        help='entity for which the context will be displayed')

    args = parser.parse_args()
    index_file = args.index_file
    corpus_file = args.corpus_file
    mapping_file = args.mapping_file
    context_size = args.context_size
    entity = args.entity

    index = load_index_file(index_file)
    mapping = load_mapping(mapping_file)

    print_context(index, entity, corpus_file, mapping, context_size)
