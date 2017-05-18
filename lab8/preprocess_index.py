import argparse
import csv
from collections import defaultdict

from operator import itemgetter


def preprocess_index(tuples_file, output_file):
    results = list()
    with open(tuples_file, 'r') as f:
        for line in f:
            # strip tuple braces '(' and ')'
            start, end, channel, name = line.strip()[1:-1].split(',')
            results.append({
                'start': start,
                'end': end,
                'channel': channel,
                'name': name.strip('"'),
            })

    sorted_by_name = sorted(results, key=itemgetter('name'))
    header = ['start', 'end', 'channel', 'name']
    with open(output_file, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for row in sorted_by_name:
            writer.writerow(row)


def load_index_file(index_file):
    index = defaultdict(list)
    with open(index_file, 'rb') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            index[row['name']].append((int(row['start']), int(row['end']), row['channel']))

    return index


def index_ambiguity(index):
    # checks whether each entity is assigned with an unique channel
    # (usually it is not the case, but when it is the processing can be made simpler)
    for entity in index:
        entity_channel = None
        for _, _, channel in index[entity]:
            if not entity_channel:
                entity_channel = channel
            elif channel != entity_channel:
                raise ValueError('Entity {} contains ambiguous channels!'.format(entity))
    print "Given index does not contain any ambiguous channels"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sort index file in tuples format by the name alphabetically")
    parser.add_argument('-i', '--input_file',
                        default='resources/potop/potop_tuples.txt',
                        help='path to file with index in tuples format')
    parser.add_argument('-o', '--output_file',
                        default='resources/potop/potop_index.txt',
                        help='path to output file containing sorted entries')

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file

    preprocess_index(input_file, output_file)
