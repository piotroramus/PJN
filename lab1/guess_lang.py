import argparse
import codecs
import os

from collections import Counter
from pprint import pprint

from corpus_definitions import languages_set
from lang_ngrams import determine_ngrams
from metrics import euclidean_metric, max_metric, cosine_metric, taxi_metric, normalize


def guess(input_file, metric, n, encoding='utf-8'):
    languages = languages_set()

    metrics = {
        'euclidean': euclidean_metric,
        'cosine': cosine_metric,
        'max': max_metric,
        'taxi': taxi_metric,
    }

    min_distance = 99999999999
    best_language = None
    distances = {}

    data = None
    with codecs.open(input_file, 'r', encoding) as f:
        data = f.read().lower()

    input_ngram = determine_ngrams(data, n)
    normalized_ngrams = normalize(input_ngram)

    for lang in languages:
        lang_stat = Counter()
        lang_file = os.path.join("results", "lang", "{}_{}.txt".format(lang, n))
        with open(lang_file, 'r') as f:
            for line in f:
                key, count = line.split(' ')
                lang_stat[key] += int(count)
        lang_stat = normalize(lang_stat)

        dist = metrics[metric](lang_stat, normalized_ngrams)

        distances[lang] = dist

        if dist < min_distance:
            min_distance = dist
            best_language = lang

    print "The best fitting language: {}".format(best_language)
    print "Distances to other languages: "
    # pprint(distances)

    return best_language


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='file with the text in language to be guessed')
    parser.add_argument('metric', help='metric used to compare languages',
                        choices=['euclidean', 'cosine', 'max', 'taxi'])
    parser.add_argument('n', help='n-gram length', type=int)
    parser.add_argument('--encoding', help='charset of input file')
    args = parser.parse_args()

    input_file = args.input_file
    metric = args.metric
    n = args.n
    encoding = 'utf-8'
    if args.encoding:
        encoding = args.encoding

    guess(input_file, metric, n, encoding)
