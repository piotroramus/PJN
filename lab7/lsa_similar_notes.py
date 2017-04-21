import argparse

from gensim import corpora, models

from utils import cosine_metric, load_preprocessed_documents, save_similar_notes


def similar_notes_by_lsa(note_id, similarity_threshold=0.3, output_file=None, model_file='resources/lsa.dat',
                         tfidf_file='resources/tfidf.dat', dictionary_file='resources/dictionary.dat',
                         processed_data_file='resources/preprocessed.txt', notes_file='resources/pap.txt'):
    print "Loading LSA model..."
    lsa_model = models.LsiModel.load(model_file)

    print "Loading tf-idf model..."
    tfidf = models.TfidfModel.load(tfidf_file)

    print "Loading words-ids dictionary..."
    dictionary = corpora.Dictionary.load(dictionary_file)

    print "Loading preprocessed data..."
    data = load_preprocessed_documents(processed_data_file)

    print "Preparing dictionary corpus..."
    corpus = [dictionary.doc2bow(document) for document in data]

    doc_tfidf = tfidf[corpus]

    print "Projecting documents into LSA space..."
    lsa_projections = lsa_model[doc_tfidf]
    doc_projection = lsa_projections[note_id]

    print "Searching for similar notes..."
    similar_notes = list()
    for i, p in enumerate(lsa_projections):
        if i == note_id:
            continue
        metric = cosine_metric(doc_projection, p)
        if metric < similarity_threshold:
            similar_notes.append(i)
    if similar_notes:
        print "Similar notes for {}: {}\n".format(note_id + 1, ', '.join(str(sn) for sn in similar_notes))
        if output_file:
            save_similar_notes(output_file, notes_file, [note_id] + similar_notes)
    else:
        print "Similar notes for threshold {} not found".format(similarity_threshold)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--notes_file',
                        default='resources/pap.txt',
                        help='path to file with notes')
    parser.add_argument('-o', '--output_file',
                        default=None,
                        help='file to save similar notes to')
    parser.add_argument('-i', '--note_id',
                        type=int,
                        required=True,
                        help='id of note to find similar notes to')
    parser.add_argument('-t', '--similarity_threshold',
                        type=float,
                        default=0.3,
                        help='threshold in [0..1] for determining notes similarity')

    args = parser.parse_args()
    similarity_threshold = args.similarity_threshold
    notes_file = args.notes_file
    output_file = args.output_file
    note_id = args.note_id - 1  # subtract one because we index from 0

    similar_notes_by_lsa(note_id=note_id, similarity_threshold=0.3, output_file=output_file, notes_file=notes_file)
