import argparse

from graph import build_graph
from tfidf import calc_idf
from utils import get_processed_documents, cosine_metric


def evaluate_tfidf_model(input_file, reference_note_id, similarity_threshold, similar_notes_ids, output):
    true_positives = 0
    true_negatives = 0
    false_negatives = 0
    false_positives = 0

    idf = calc_idf(input_file)
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

    with open(output, 'w') as f:
        f.write("TFIDF: \n")
        f.write("precision:\t{}\n".format(precision))
        f.write("recall:\t{}\n".format(recall))
        f.write("f1:\t{}\n\n".format(f1))


def evaluate_graph_model(input_file, reference_note_id, k, similarity_threshold, similar_notes_ids, output):
    true_positives = 0
    true_negatives = 0
    false_negatives = 0
    false_positives = 0

    documents = get_processed_documents(input_file, apply_stoplist=True)

    graphs = dict()
    for note_id, document in enumerate(documents):
        graphs[note_id] = build_graph(document, k)
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

    with open(output, 'w') as f:
        f.write("Graph of {} order: \n".format(k))
        f.write("precision:\t{}\n".format(precision))
        f.write("recall:\t{}\n".format(recall))
        f.write("f1:\t{}\n\n".format(f1))


def load_similar_notes_ids(input_file):
    raise NotImplementedError()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file',
                        default='resources/pap.txt',
                        help='path to file with input data')
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
                        default=0.65,
                        help='threshold in [0..1] for determining notes similarity')

    args = parser.parse_args()
    similarity_threshold = args.similarity_threshold
    input_file = args.input_file
    output_file = args.output_file
    reference_note_id = args.note_id - 1  # subtract one because we index from 0
    reference_notes_file = args.reference_notes

    similar_notes_ids = load_similar_notes_ids(reference_notes_file)
    evaluate_tfidf_model(input_file, reference_note_id, similarity_threshold, similar_notes_ids, output_file)

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
        evaluate_graph_model(input_file, reference_note_id, params['k'], params['similarity_threshold'], similar_notes_ids, output_file)
