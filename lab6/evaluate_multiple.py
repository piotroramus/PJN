import argparse
import os

from graph import build_graph
from tfidf import calc_idf
from utils import get_processed_documents, cosine_metric


def evaluate_tfidf_model(input_file, similarity_threshold, similar_notes, output):
    true_positives = 0
    true_negatives = 0
    false_negatives = 0
    false_positives = 0

    reference_notes = similar_notes.keys()
    idf = calc_idf(input_file)

    for reference_note_id in reference_notes:

        similar_notes_ids = similar_notes[reference_note_id]
        ref_note_idf = idf[reference_note_id]
        for note_id in range(len(idf)):
            if note_id == reference_note_id:
                continue
            metric = cosine_metric(idf[note_id], ref_note_idf)
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

    with open(output, 'a+') as f:
        f.write("TFIDF: \n")
        f.write("TP;FN;FP;TN: {};{};{};{}\n".format(true_positives, false_negatives, false_positives, true_negatives))
        f.write("precision:\t{}\n".format(precision))
        f.write("recall:\t{}\n".format(recall))
        f.write("f1:\t{}\n\n".format(f1))


def evaluate_graph_model(input_file, k, similarity_threshold, similar_notes, output):
    true_positives = 0
    true_negatives = 0
    false_negatives = 0
    false_positives = 0

    documents = get_processed_documents(input_file, apply_stoplist=True)

    graphs = dict()
    for note_id, document in enumerate(documents):
        graphs[note_id] = build_graph(document, k)

    reference_notes = similar_notes.keys()

    for reference_note_id in reference_notes:
        similar_notes_ids = similar_notes[reference_note_id]
        ref_graph = graphs[reference_note_id]

        for note_id in graphs:
            if note_id == reference_note_id:
                continue
            graph = graphs[note_id]
            metric = cosine_metric(graph, ref_graph)

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

    with open(output, 'a+') as f:
        f.write("Graph of order {}: \n".format(k))
        f.write("TP;FN;FP;TN: {};{};{};{}\n".format(true_positives, false_negatives, false_positives, true_negatives))
        f.write("precision:\t{}\n".format(precision))
        f.write("recall:\t{}\n".format(recall))
        f.write("f1:\t{}\n\n".format(f1))


def load_similar_notes_ids(reference_notes_dir):
    input_files = os.listdir(reference_notes_dir)

    similar_notes = dict()
    for file in input_files:
        similar_notes[int(file) - 1] = list()
        with open(os.path.join(reference_notes_dir, file), 'r') as f:
            for line in f:
                if line.strip() != file:
                    similar_notes[int(file) - 1].append(int(line) - 1)

    return similar_notes


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file',
                        default='resources/pap.txt',
                        help='path to file with input data')
    parser.add_argument('-o', '--output_file',
                        default='results/binary_classification_multiple.txt',
                        help='file to save evaluation results')
    parser.add_argument('--reference_notes_dir',
                        default='results/similar_ref/',
                        help='path to file with ids of rerefence notes similar to the specified id')

    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    reference_notes_dir = args.reference_notes_dir

    similar_notes = load_similar_notes_ids(reference_notes_dir)

    tfidf_similarity_threshold = 0.5
    evaluate_tfidf_model(input_file, tfidf_similarity_threshold, similar_notes, output_file)

    # determined experimentally
    testing_params = [
        {
            'k': 2,
            'similarity_threshold': 0.65
        },
        {
            'k': 3,
            'similarity_threshold': 0.65
        },
        {
            'k': 5,
            'similarity_threshold': 0.7
        },
    ]

    for params in testing_params:
        evaluate_graph_model(input_file, params['k'], params['similarity_threshold'], similar_notes, output_file)
