# -*- coding: utf-8 -*-

import argparse
import os
from collections import Counter

from preprocess_index import load_index_file


def make_stats(index, out_dir):
    # prepares 3 kinds of stats:
    # general: entity with overall number of appearances
    # 2-categorized: 10 most common names and places
    # 5-categorized: 10 most common entities in each of 5nam model category

    categories_5nam = {
        'names': ['person_last_nam', 'person_first_nam'],
        'places': ['country_nam', 'city_nam', 'road_nam']
    }
    categories = categories_5nam

    overall_file = os.path.join(out_dir, 'overall.txt')
    two_categories_file = os.path.join(out_dir, '2_cat.txt')
    five_categories_file = os.path.join(out_dir, '5_cat.txt')

    # sort index by the number of name appearances in corpus
    sorted_index = sorted(index, key=lambda k: len(index[k]), reverse=True)

    # save overall stats
    print "Saving overall stats to {}...".format(overall_file)
    with open(overall_file, 'w') as f:
        for entity in sorted_index:
            f.write("{}: {}\n".format(entity, len(index[entity])))

    # determine and save 2-categorized index
    names_index = Counter()
    places_index = Counter()
    for entity in sorted_index:
        for _, _, channel in index[entity]:
            if channel in categories['names']:
                names_index[entity] += 1
            elif channel in categories['places']:
                places_index[entity] += 1
            else:
                raise ValueError('Unknown channel {} for entity {}'.format(channel, entity))
    print "Saving 2-categorized stats to {}...".format(two_categories_file)
    with open(two_categories_file, 'w') as f:
        f.write("=======================\n")
        f.write("10 most common names:\n")
        for entity, count in names_index.most_common(10):
            f.write("{}: {}\n".format(entity, count))
        f.write("=======================\n")
        f.write("10 most common places:\n")
        for entity, count in places_index.most_common(10):
            f.write("{}: {}\n".format(entity, count))

    # determine and save 5-categorized index
    channel_index = dict()
    individual_channels = [cat for subl in categories_5nam.values() for cat in subl]
    for c in individual_channels:
        channel_index[c] = Counter()
    for entity in sorted_index:
        for _, _, channel in index[entity]:
            channel_index[channel][entity] += 1
    print "Saving 5-categorized stats to {}...".format(five_categories_file)
    with open(five_categories_file, 'w') as f:
        for channel in individual_channels:
            f.write("=======================\n")
            f.write("10 most common {}:\n".format(channel))
            for entity, count in channel_index[channel].most_common(10):
                f.write("{}: {}\n".format(entity, count))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Prints context of the given entity')
    parser.add_argument('--index_file',
                        default='resources/potop/potop_index.txt',
                        help='path to file containing indexed entities')
    parser.add_argument('--output_dir',
                        default='results/',
                        help='directory to saved results to')

    args = parser.parse_args()
    index_file = args.index_file
    output_dir = args.output_dir

    index = load_index_file(index_file)
    make_stats(index, output_dir)
