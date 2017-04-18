import io
import re
import string

from plp import PLP

plp = PLP()


def basic_form(word):
    ids = plp.rec(word)
    if not ids:
        return word
    return plp.bform(ids[0])


def cosine_metric(v1, v2):
    keys = set(v1.keys()) & set(v2.keys())
    s = 0
    for key in keys:
        s += v1.get(key, 0) * v2.get(key, 0)
    return 1 - s


def get_processed_documents(filename, output=None, encoding='utf-8'):
    remove_punctuation_pattern = re.compile('[%s]' % re.escape(string.punctuation))

    print "Processing {}".format(filename)
    documents = documents_to_list(filename, encoding)

    processed_documents = [doc.strip().lower() for doc in documents]
    processed_documents = [remove_punctuation_pattern.sub(' ', doc) for doc in processed_documents]

    if output:
        print "Saving processed documents to {}".format(output)
        with io.open(output, 'w', encoding=encoding) as f:
            for i, document in enumerate(processed_documents):
                f.write(u'#{:06}\n'.format(i))
                f.write(document)

    return processed_documents


def documents_to_list(filename, encoding='utf-8'):
    new_doc_pattern = r'#\d{6}'
    new_doc_split = re.compile(new_doc_pattern)
    with io.open(filename, 'r', encoding=encoding) as f:
        documents = re.split(new_doc_split, f.read())[1:]
    return documents


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
