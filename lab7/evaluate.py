import argparse
import io
import re

from gensim import corpora, models
from utils import load_preprocessed_documents, cosine_metric


def evaluate_lsa_model(reference_note_id, similarity_threshold, similar_notes_ids, output_file):
    model_file = 'resources/lsa.dat'
    tfidf_file = 'resources/tfidf.dat'
    dictionary_file = 'resources/dictionary.dat'
    processed_data_file = 'resources/preprocessed.txt'

    print "Preparing data..."
    lsa_model = models.LsiModel.load(model_file)
    tfidf = models.TfidfModel.load(tfidf_file)
    dictionary = corpora.Dictionary.load(dictionary_file)
    data = load_preprocessed_documents(processed_data_file)
    corpus = [dictionary.doc2bow(document) for document in data]
    doc_tfidf = tfidf[corpus]
    lsa_projections = lsa_model[doc_tfidf]

    true_positives = 0
    true_negatives = 0
    false_negatives = 0
    false_positives = 0

    print "Evaluating..."
    reference_projection = lsa_projections[reference_note_id]
    for note_id, p in enumerate(lsa_projections):
        if note_id == reference_note_id:
            continue
        metric = cosine_metric(reference_projection, p)
        if note_id in similar_notes_ids:
            if metric < similarity_threshold:
                true_positives += 1
            else:
                false_negatives += 1
        else:
            if metric < similarity_threshold:
                false_positives += 1
            else:
                true_negatives += 1

    precision = true_positives / float(true_positives + false_positives)
    recall = true_positives / float(true_positives + false_negatives)
    f1 = 2 * ((precision * recall) / float(precision + recall))

    print "Saving results to {}...".format(output_file)
    with open(output_file, 'a+') as f:
        f.write("LSA: \n")
        f.write("TP;FN;FP;TN: {};{};{};{}\n".format(true_positives, false_negatives, false_positives, true_negatives))
        f.write("precision:\t{}\n".format(precision))
        f.write("recall:\t{}\n".format(recall))
        f.write("f1:\t{}\n\n".format(f1))


def load_similar_notes_ids(input_file, encoding='utf-8'):
    note_id_pattern = r'#\d{6}'
    note_id_line = re.compile(note_id_pattern)
    note_ids = list()

    with io.open(input_file, 'r', encoding=encoding) as f:
        for line in f:
            if note_id_line.match(line):
                note_id = int(line.strip()[1:]) - 1
                note_ids.append(note_id)

    return note_ids


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output_file',
                        default='results/binary_classification.txt',
                        help='file to save evaluation results')
    parser.add_argument('-i', '--note_id',
                        type=int,
                        required=True,
                        help='reference note id')
    parser.add_argument('--reference_notes',
                        default='results/selected_reference_notes.txt',
                        help='path to file with ids of rerefence notes similar to the specified id')
    parser.add_argument('-t', '--similarity_threshold',
                        type=float,
                        default=0.3,
                        help='threshold in [0..1] for determining notes similarity')

    args = parser.parse_args()
    output_file = args.output_file
    reference_note_id = args.note_id - 1  # subtract one because we index from 0
    reference_notes_file = args.reference_notes
    similarity_threshold = args.similarity_threshold

    similar_notes_ids = load_similar_notes_ids(reference_notes_file)

    evaluate_lsa_model(reference_note_id, similarity_threshold, similar_notes_ids, output_file)
