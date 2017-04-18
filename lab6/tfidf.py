# -*- coding: utf-8 -*-

from __future__ import division

import argparse
from collections import Counter, defaultdict
from math import sqrt, fsum, log

from utils import basic_form, cosine_metric
from utils import get_processed_documents, documents_to_list
from utils import save_similar_notes


def calc_idf(filename, encoding='utf-8'):
    global_tf = dict()
    global_idf = dict()
    df = Counter()
    documents = get_processed_documents(filename, encoding=encoding)
    N = len(documents)

    print "Calculating TF and DF..."
    for document_nr, document in enumerate(documents):
        tf = Counter()
        for word in document.split():
            bform = basic_form(word)
            tf[bform] += 1
        global_tf[document_nr] = tf
        for word in tf.keys():
            df[word] += tf[word]

    print "Calculating IDF..."
    for document_nr in xrange(N):
        idf = defaultdict(float)
        for word, word_tf in global_tf[document_nr].items():
            idf[word] = word_tf * (log(N / df[word]))
        normalized_idf = defaultdict(float)
        norm = sqrt(fsum([val * val for val in idf.values()]))
        for key, val in idf.items():
            normalized_idf[key] = val / norm
        global_idf[document_nr] = normalized_idf

    return global_idf


def print_note(note_id, filename, encoding='utf-8'):
    documents = documents_to_list(filename, encoding)
    print documents[note_id]


def find_similar_notes(input_file, output_file, note_id, similarity_threshold):
    idf = calc_idf(input_file)
    note_idf = idf[note_id]
    similar_notes = []
    for i in range(len(idf)):
        if i == note_id:
            continue
        metric = cosine_metric(idf[i], note_idf)
        if metric < similarity_threshold:
            similar_notes.append(i)
    if similar_notes:
        print "Similar notes for {}: {}\n".format(note_id + 1, ', '.join(str(sn) for sn in similar_notes))
        if output_file:
            save_similar_notes(output_file, input_file, [note_id] + similar_notes)
    else:
        print "Similar notes for threshold {} not found".format(similarity_threshold)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file',
                        default='resources/pap.txt',
                        help='path to file with input data')
    parser.add_argument('-o', '--output_file',
                        default=None,
                        help='file to save similar notes to')
    parser.add_argument('-i', '--note_id',
                        type=int,
                        required=True,
                        help='id of note to find similar notes to')
    parser.add_argument('-t', '--similarity_threshold',
                        type=float,
                        default=0.5,
                        help='threshold in [0..1] for determining notes similarity')

    args = parser.parse_args()
    similarity_threshold = args.similarity_threshold
    input_file = args.input_file
    output_file = args.output_file
    note_id = args.note_id - 1  # subtract one because we index from 0

    find_similar_notes(input_file, output_file, note_id, similarity_threshold)
