import argparse
from collections import Counter
from collections import defaultdict
from math import sqrt, fsum

from utils import get_processed_documents, save_similar_notes, cosine_metric


def build_graph(document, k):
    """ A graph is simply represented by a Counter simulating list of adjacency with edges arity"""
    graph = Counter()
    doc_len = len(document)
    for start in xrange(doc_len):
        end = min(start + k + 1, doc_len)
        for v in document[start:end]:
            graph[(document[start], v)] += 1

    normalized_graph = defaultdict(float)
    norm = sqrt(fsum([val * val for val in graph.values()]))
    for key, val in graph.items():
        normalized_graph[key] = val / norm

    return normalized_graph


def find_similar_notes(input_file, output_file, note_id, k, similarity_threshold):
    """ Suitable for invoking only once (not in a loop!) - it builds all the things each time invoked"""
    documents = get_processed_documents(input_file, apply_stoplist=True)

    print "Building graphs..."
    ref_graph = build_graph(documents[note_id], k)
    similar_notes = list()
    for i, document in enumerate(documents):
        if i == note_id:
            continue
        graph = build_graph(document, k)
        dist = cosine_metric(graph, ref_graph)

        if dist < similarity_threshold:
            similar_notes.append((i, dist))

    if similar_notes:
        print "Similar notes for {}: {}\n".format(note_id + 1, ', '.join(str(sn) for sn, _ in similar_notes))
        if output_file:
            note_ids = [k for k, v in similar_notes]
            save_similar_notes(output_file, input_file, [note_id] + note_ids)
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
    parser.add_argument('-k',
                        type=int,
                        default=2,
                        help='graph order')
    parser.add_argument('-t', '--similarity_threshold',
                        type=float,
                        default=0.5,
                        help='threshold in [0..1] for determining notes similarity')

    args = parser.parse_args()
    similarity_threshold = args.similarity_threshold
    input_file = args.input_file
    output_file = args.output_file
    note_id = args.note_id - 1  # subtract one because we index from 0
    k = args.k

    find_similar_notes(input_file, output_file, note_id, k, similarity_threshold)
