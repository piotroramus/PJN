# coding=utf-8

import argparse
import codecs
import re

from collections import Counter
from collections import defaultdict

from levenshtein import modified_levenshtein_distance

only_letters_pattern = re.compile("[^\w]", re.UNICODE)


def build_corpus_stats(input_list, number_of_forms, output_file):
    stats = Counter()

    for input_file in input_list:
        with codecs.open(input_file, 'r', 'utf-8') as f:
            for line in f:
                for word in line.strip().split():
                    word = only_letters_pattern.sub('', word).lower()
                    if word == '':
                        continue
                    stats[word] += 1

    alpha = 1.0
    all_sum = sum(stats.values()) + alpha * number_of_forms
    res_with_additive_smooting = defaultdict(lambda: alpha / all_sum)
    res_with_additive_smooting.update({word: (stats[word] + alpha) / all_sum for word in stats})

    with codecs.open(output_file, 'w', encoding='utf-8') as f:
        for stat in res_with_additive_smooting:
            f.write(stat + ',' + str(res_with_additive_smooting[stat]) + '\n')
    print "Corpus stats saved to {}".format(output_file)

    return res_with_additive_smooting


def build_error_stats(input_list, output_file):
    distances = Counter()

    for input_file in input_list:
        with codecs.open(input_file, 'r', 'utf-8') as f:
            for line in f:
                word_with_error, proper_word = line.strip().split(';')
                word_with_error = only_letters_pattern.sub('', word_with_error).lower()
                proper_word = only_letters_pattern.sub('', proper_word).lower()
                if word_with_error == '' or proper_word == '':
                    continue
                distances[modified_levenshtein_distance(word_with_error, proper_word)] += 1

    errors_sum = float(sum(distances.values()))
    # take into account 0 distance which should be superior to other errors
    distances[0] = errors_sum
    errors_sum *= 2
    result = defaultdict(int)

    with open(output_file, 'w') as f:
        for dist in distances:
            result[dist] = distances[dist] / errors_sum
            f.write("{},{}\n".format(dist, result[dist]))
    print "Error stats saved to {}".format(output_file)

    return result


def load_corpus_and_error_stats(corpus_stats_file, error_stats_file):
    print "Loading stats from disk..."
    corpus_stats = defaultdict(int)
    with codecs.open(corpus_stats_file, 'r', encoding='utf-8') as f:
        for line in f:
            word, value = line.split(',')
            corpus_stats[word] = float(value)

    error_stats = defaultdict(int)
    with open(error_stats_file) as f:
        for line in f:
            dist, value = map(float, line.split(','))
            error_stats[dist] = value

    print "Corpus and error stats loaded"

    return corpus_stats, error_stats


def load_forms(input_list):
    forms = list()
    for input_file in input_list:
        with codecs.open(input_file, 'r', 'utf-8') as f:
            for line in f:
                forms.append(line.strip())
    return forms


def error_probability(word, correction, error_stats):
    distance = modified_levenshtein_distance(word, correction)
    return error_stats[distance]


def correct_word(word, corpus_stats, error_stats, corrections, max_matches=10, max_length_diff=1,
                 corpus_factor=0.5):
    print "Determining possible word corrections..."
    probable_corrections = Counter()
    for c in corrections:
        if abs(len(word) - len(c)) <= max_length_diff:
            probable_corrections[c] = error_probability(word, c, error_stats) * (corpus_stats[c] ** corpus_factor)
    return probable_corrections.most_common(max_matches)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('word', help='word to correct')
    parser.add_argument('--perform_preprocessing',
                        help='compute error and corpus stats instead of reading it from file',
                        action='store_true')
    parser.add_argument('--corpus_stats_file', help='path to file with precomputed corpus stats')
    parser.add_argument('--error_stats_file', help='path to file with precomputed error stats')
    parser.add_argument('-n', '--max_matches', help='maximum number of word corrections to display', type=int)
    args = parser.parse_args()

    defaults = {
        'perform_preprocessing': False,
        'corpus_stats_file': 'resources/corpus_stats.txt',
        'error_stats_file': 'resources/error_stats.txt',
        'simple': False,
        'max_matches': 20,
    }

    word_to_correct = unicode(args.word, 'utf-8')
    perform_preprocessing = args.perform_preprocessing or defaults['perform_preprocessing']
    corpus_stats_file = args.corpus_stats_file or defaults['corpus_stats_file']
    error_stats_file = args.error_stats_file or defaults['error_stats_file']
    max_matches = args.max_matches or defaults['max_matches']

    corpus_files = [
        "resources/dramat.txt",
        "resources/popul.txt",
        "resources/proza.txt",
        "resources/publ.txt",
        "resources/wp.txt",
    ]
    error_files = ["resources/bledy.txt"]
    forms_files = ["resources/formy.txt"]

    forms = load_forms(forms_files)
    number_of_forms = len(forms)

    if perform_preprocessing:
        print "Performing preprocessing..."
        corpus_stats = build_corpus_stats(corpus_files, number_of_forms, output_file=corpus_stats_file)
        error_stats = build_error_stats(error_files, output_file=error_stats_file)
    else:
        corpus_stats, error_stats = load_corpus_and_error_stats(corpus_stats_file, error_stats_file)

    proposed_corrections = correct_word(word_to_correct, corpus_stats, error_stats, forms, max_matches=max_matches)

    print "Proposed correction: probability"
    for correction, probability in proposed_corrections:
        print correction.encode('utf-8') + ": " + str(probability)
