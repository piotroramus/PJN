import argparse
import codecs
import re

from pprint import pprint
from unidecode import unidecode

from metrics import levenshtein_metric, longest_common_subsequence_metric, longest_common_substring_metric


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


def apply_stoplist(stoplist, data):
    pass


def preprocess(line):
    only_letters_and_digits = re.compile("[^a-z0-9\s]")
    multiple_whitespaces = re.compile('\s+')

    line = unidecode(line.strip().lower())
    line = only_letters_and_digits.sub(' ', line)
    line = multiple_whitespaces.sub(' ', line.strip())

    # TODO: apply stoplist
    return line


def clusterize(metric=None, similarity_threshold=None, input_file=None):
    if not metric:
        metric = 'longest_common_subsequence'
    if not similarity_threshold:
        similarity_threshold = 0.5
    if not input_file:
        input_file = "resources/lines.txt"

    # TODO: either move to parameters or remove
    preprocessing_results = 'preprocessed.txt'
    results_file = 'out.txt'

    metrics = {
        'levenshtein': levenshtein_metric,
        'longest_common_substring': longest_common_substring_metric,
        'longest_common_subsequence': longest_common_subsequence_metric,
    }
    metric = metrics[metric]

    # TODO: I want to refeactor this
    with open(preprocessing_results, 'w') as outf:
        with codecs.open(input_file, 'r', 'utf-8') as f:
            for line in f:
                line = preprocess(line)
                outf.write("{}\n".format(line))

    clusters = dict()
    cluster_num = 0

    with open(preprocessing_results, 'r') as pf:
        for line in pf:
            match = False
            for cluster_num in clusters:
                for entry in clusters[cluster_num]:
                    if metric(entry, line) < similarity_threshold:
                        match = True
                        clusters[cluster_num].append(line)
                        break

                # to avoid subscribing for multiple clusters
                if match:
                    break

            if not match:
                cluster_num += 1
                clusters[cluster_num] = [line]

    # TODO: this probably will not be needed? not sure... maybe it would be better to divide clusterize and quality check...
    with open(results_file, 'w') as rf:
        for cluster in clusters:
            rf.write("##########\n")
            for line in clusters[cluster]:
                rf.write(line)
            rf.write("\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--metric',
                        help='metric used to compare strings',
                        choices=['levenshtein', 'longest_common_substring', 'longest_common_subsequence'])
    parser.add_argument('--similarity_threshold',
                        help='float value of [0..1] determining whether two strings are similar or not', type=float)
    parser.add_argument('--input_file',
                        help='path to file with strings to clusterize')
    args = parser.parse_args()

    metric = args.metric
    similarity_threshold = args.similarity_threshold
    input_file = args.input_file

    clusterize(metric, similarity_threshold, input_file)
