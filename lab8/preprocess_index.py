import argparse
import csv

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
        for row in sorted_by_name:
            writer.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sort index file in tuples format by the name alphabetically")
    parser.add_argument('-i', '--input_file',
                        default='resources/potop_tuples.txt',
                        help='path to file with index in tuples format')
    parser.add_argument('-o', '--output_file',
                        default='resources/potop_index.txt',
                        help='path to output file containing sorted entries')

    args = parser.parse_args()
    # input_file = args.input_file
    input_file = 'potop_tuples_small.txt'
    output_file = args.output_file

    preprocess_index(input_file, output_file)
