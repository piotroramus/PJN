import argparse

from utils import load_preprocessed_documents, preprocess_documents
from gensim import corpora, models


def build_words_ids_dictionary(output_file='resources/dictionary.dat'):
    print "Loading preprocessed data..."
    data = load_preprocessed_documents(processed_data_file)

    print "Building words-ids dictionary..."
    dictionary = corpora.Dictionary(data)

    print "Filtering out hapax legomena and words appearing in more than 70% of documents..."
    dictionary.filter_extremes(no_below=2, no_above=0.7, keep_n=200000)

    print "Shrinking dictionary..."
    dictionary.compactify()

    print "Saving dictionary..."
    dictionary.save(output_file)


def build_tf_idf_model(output_file='resources/tfidf.dat', dictionary_file='resources/dictionary.dat'):
    print "Loading preprocessed data..."
    data = load_preprocessed_documents(processed_data_file)

    print "Loading words-ids dictionary..."
    dictionary = corpora.Dictionary.load(dictionary_file)

    print "Preparing corpus for calculating tf-idf..."
    corpus = [dictionary.doc2bow(document) for document in data]

    print "Calculating TF-IDF model..."
    tfidf = models.TfidfModel(corpus)

    print "Saving tfidf model..."
    tfidf.save(output_file)


def calculate_lsa(output_file, processed_data_file, dictionary_file='resources/dictionary.dat',
                  tfidf_file='resources/tfidf.dat'):
    print "Loading preprocessed data..."
    data = load_preprocessed_documents(processed_data_file)

    print "Loading words-ids dictionary..."
    dictionary = corpora.Dictionary.load(dictionary_file)

    print "Loading tf-idf model..."
    tfidf = models.TfidfModel.load(tfidf_file)

    print "Preparing dictionary corpus..."
    corpus = [dictionary.doc2bow(document) for document in data]

    print "Calculating LSA model..."
    lsa_model = models.LsiModel(corpus=tfidf[corpus], num_topics=1000, id2word=dictionary)

    print "Saving LSA model..."
    lsa_model.save(output_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--action',
                        choices=['preprocessing', 'dict', 'tfidf', 'lsa'],
                        default='lsa',
                        help='action to be taken')
    parser.add_argument('-o', '--lsa_output',
                        default='resources/lsa.dat',
                        help='path to file storing resulting LSA model for lsa action')
    parser.add_argument('--processed_data',
                        default='resources/preprocessed.txt',
                        help='path to file containing preprocessed data for lsa action')
    parser.add_argument('--raw_data',
                        default='resources/pap.txt',
                        help='path to file with unprocessed corpus for preprocessing action')

    args = parser.parse_args()

    action = args.action
    lsa_output = args.lsa_output
    processed_data_file = args.processed_data
    raw_data_file = args.raw_data

    if action == 'preprocessing':
        preprocess_documents(filename=raw_data_file)
    elif action == 'dict':
        build_words_ids_dictionary()
    elif action == 'tfidf':
        build_tf_idf_model()
    elif action == 'lsa':
        calculate_lsa(lsa_output, processed_data_file)
