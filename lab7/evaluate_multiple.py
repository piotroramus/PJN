import argparse
import os

from gensim import corpora, models
from utils import load_preprocessed_documents, cosine_metric


def evaluate_lsa_model(similarity_threshold, similar_notes, output_file):
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

    reference_notes = similar_notes.keys()

    print "Evaluating..."
    for reference_note_id in reference_notes:
        print "Evaluating {}...".format(reference_note_id + 1)

        similar_notes_ids = similar_notes[reference_note_id]
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
    parser.add_argument('-o', '--output_file',
                        default='results/binary_classification_multiple.txt',
                        help='file to save evaluation results')
    parser.add_argument('--reference_notes_dir',
                        default='results/similar_ref',
                        help='path to dir with reference similar notes ids')
    parser.add_argument('-t', '--similarity_threshold',
                        type=float,
                        default=0.3,
                        help='threshold in [0..1] for determining notes similarity')

    args = parser.parse_args()
    output_file = args.output_file
    reference_notes_dir = args.reference_notes_dir
    similarity_threshold = args.similarity_threshold

    similar_notes = load_similar_notes_ids(reference_notes_dir)

    evaluate_lsa_model(similarity_threshold, similar_notes, output_file)
