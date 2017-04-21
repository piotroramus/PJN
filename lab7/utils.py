import io
import re
import string

from math import fsum, sqrt
from plp import PLP
from stoplist import load_stoplist, apply_stoplist_to_doc

plp = PLP()


def basic_form(word):
    ids = plp.rec(word)
    if not ids:
        return word
    return plp.bform(ids[0])


def _norm(v):
    s = fsum([v * v for v in v.values()])
    return sqrt(s)


def cosine_metric(v1, v2):
    # convert tuple to dict
    v1 = {k: v for k, v in v1}
    v2 = {k: v for k, v in v2}

    keys = set(v1.keys()) & set(v2.keys())
    norm = _norm(v1) * _norm(v2)
    try:
        s = fsum([float(v1[key] * v2[key]) / norm for key in keys])
    except ZeroDivisionError:
        s = 0
    return 1 - s


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


def save_similar_notes(output_file, notes_file, note_ids):
    documents = documents_to_list(notes_file)

    print "Saving similar notes to {}...".format(output_file)
    with io.open(output_file, 'w', encoding='utf-8') as f:
        f.write(u'#{:06} - REFERENCE NOTE'.format(note_ids[0] + 1))
        f.write(documents[note_ids[0]])
        f.write(u'\n')
        for note_id in note_ids[1:]:
            f.write(u'#{:06}'.format(note_id + 1))
            f.write(documents[note_id])
            f.write(u'\n')
