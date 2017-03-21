import argparse
import codecs
import re

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


def apply_stoplist(line, stoplist):
    for word in stoplist:
        # this is to ensure that the whole word is being replaced, not a part (like 'me' in 'some')
        pattern = re.compile("(^{}\s)|(\s{}\s)|(\s{}$)".format(word, word, word))
        line = pattern.sub(' ', line)
    return line


def preprocess_line(line, stoplist):
    only_letters_and_digits = re.compile("[^a-z0-9\s]")
    multiple_whitespaces = re.compile('\s+')

    line = unidecode(line.strip().lower())
    line = only_letters_and_digits.sub(' ', line)

    apply_stoplist(line, stoplist)

    line = multiple_whitespaces.sub(' ', line.strip())

    return line


def preprocess(input_file, output_file):
    stoplist = load_stoplist()
    with open(output_file, 'w') as outf:
        with codecs.open(input_file, 'r', 'utf-8') as f:
            for line in f:
                line = preprocess_line(line, stoplist)
                outf.write("{}\n".format(line))


def clusterize(metric=None, similarity_threshold=None, input_file=None, output_file=None, perform_preprocessing=None,
               preprocessing_results=None):
    if not metric:
        metric = 'longest_common_subsequence'
    if not similarity_threshold:
        similarity_threshold = 0.5
    if not input_file:
        input_file = "resources/lines.txt"
    if not output_file:
        output_file = 'out_{}_{}.txt'.format(metric, str(similarity_threshold).replace('.', '_'))
    if not preprocessing_results:
        preprocessing_results = 'preprocessed.txt'

    metrics = {
        'levenshtein': levenshtein_metric,
        'longest_common_substring': longest_common_substring_metric,
        'longest_common_subsequence': longest_common_subsequence_metric,
    }
    metric = metrics[metric]

    if perform_preprocessing:
        preprocess(input_file, preprocessing_results)

    clusters = dict()
    cluster_num = 0

    with open(preprocessing_results, 'r') as pf:
        line_num = 0
        for line in pf:
            line_num += 1
            print "Processing line {}...\n".format(line_num)
            match = False
            for cluster_num in clusters:
                if metric(clusters[cluster_num][0], line) < similarity_threshold:
                    match = True
                    clusters[cluster_num].append(line)
                    break

            if not match:
                cluster_num += 1
                clusters[cluster_num] = [line]

    with open(output_file, 'w') as rf:
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
    parser.add_argument('--output_file',
                        help='path to file where the results will be stored')
    parser.add_argument('--perform_preprocessing',
                        help='perform preprocessing')
    parser.add_argument('--preprocessing_results',
                        help='path to file where results of preprecessing will be stored (when done on the fly) '
                             'or taken from (if done in advance) and applied')

    args = parser.parse_args()

    metric = args.metric
    similarity_threshold = args.similarity_threshold
    input_file = args.input_file
    output_file = args.output_file
    perform_preprocessing = args.perform_preprocessing
    preprocessing_results = args.preprocessing_results

    clusterize(metric, similarity_threshold, input_file, output_file, perform_preprocessing, preprocessing_results)
