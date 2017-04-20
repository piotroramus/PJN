import io
import re
import string

from plp import PLP
from stoplist import load_stoplist, apply_stoplist_to_doc

plp = PLP()


def basic_form(word):
    ids = plp.rec(word)
    if not ids:
        return word
    return plp.bform(ids[0])


def document_in_basic_form(document):
    return [basic_form(word) for word in document]


def documents_to_list(filename, encoding='utf-8'):
    new_doc_pattern = r'#\d{6}'
    new_doc_split = re.compile(new_doc_pattern)
    with io.open(filename, 'r', encoding=encoding) as f:
        documents = re.split(new_doc_split, f.read())[1:]
    return documents


def load_preprocessed_documents(filename='resources/preprocessed.txt', encoding='utf-8'):
    documents = list()
    with io.open(filename, 'r', encoding=encoding) as f:
        for line in f:
            documents.append(line.split())
    return documents


def preprocess_documents(filename, encoding='utf-8', output='resources/preprocessed.txt'):
    remove_punctuation_pattern = re.compile('[%s]' % re.escape(string.punctuation))

    print "Processing {}...".format(filename)
    documents = documents_to_list(filename, encoding)

    print "Making everything lowercase..."
    processed_documents = [doc.strip().lower() for doc in documents]

    print "Removing punctuation..."
    processed_documents = [remove_punctuation_pattern.sub(' ', doc).split() for doc in processed_documents]

    print "Bringing all words to basic form..."
    processed_documents = [document_in_basic_form(doc) for doc in processed_documents]

    print "Applying stoplist..."
    stoplist = load_stoplist()
    processed_documents = [apply_stoplist_to_doc(stoplist, doc) for doc in processed_documents]

    print "Removing empty documents..."
    processed_documents = [doc for doc in processed_documents if doc]

    print "File preprocessing done. Saving results to {}...".format(output)
    with io.open(output, 'w', encoding=encoding) as f:
        for document in processed_documents:
            for word in document:
                f.write(u"{} ".format(word))
            f.write(u'\n')
