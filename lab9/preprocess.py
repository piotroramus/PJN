# coding: utf-8

import csv
import io
import re
import string

from collections import defaultdict, Counter

from PlpWrapper import PlpWrapper, GrammarCase, PartOfSpeech

import sys

# nasty hack, but I did not have time to fix encodings the proper way
reload(sys)
sys.setdefaultencoding('utf-8')

plp = PlpWrapper()


def split_to_sentences(input_file):
    new_doc_pattern = r'#\d{6}'
    new_doc_split = re.compile(new_doc_pattern)

    sentence_pattern = r'\.\s+(?=[A-ZĆŁŚŻŹ])'
    sentence_split = re.compile(sentence_pattern)

    remove_punctuation_pattern = re.compile('[%s]' % re.escape(string.punctuation))

    sentences = list()
    with io.open(input_file, 'r', encoding='utf-8') as f:
        documents = re.split(new_doc_split, f.read())[1:]
        for doc in documents:
            for sentence in re.split(sentence_split, doc):
                processed = remove_punctuation_pattern.sub(' ', sentence.strip()).lower()
                sentences.append(processed)

    return sentences


def prepositions(sentences, output_file='results/prepositions.csv'):
    print "Determining prepositions followed by noun..."
    result = defaultdict(set)

    for sentence in sentences:
        words = sentence.strip().split(' ')

        word_index = 0
        words_len = len(words)
        while word_index < words_len:
            word = words[word_index].strip()
            prep = plp.get_preposition(word)
            if not prep:
                word_index += 1
                continue

            # look until noun is encountered or sentence is over
            next_word_index = word_index + 1
            loop = True
            while loop and next_word_index < words_len:
                next_word = words[next_word_index]
                next_word_index += 1
                next_word_nouns = plp.get_noun_ids(next_word)
                for noun in next_word_nouns:
                    loop = False
                    result[word].add((next_word, noun))
            word_index += 1

    # print "Saving prepositions map to {}...".format(output_file)
    with io.open(output_file, 'wb') as f:
        writer = csv.writer(f, delimiter=";")
        for prep in result:
            row = [unicode(prep)]
            for noun, clp_id in result[prep]:
                row.append(unicode(noun))
                row.append(unicode(clp_id))
            writer.writerow(row)

    print "Done"
    return result


def load_prepositions(input_file='results/prepositions.csv'):
    print "Loading prepositions map from {}".format(input_file)

    prep_map = defaultdict(set)
    with io.open(input_file, 'rb') as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            preposition = row[0]
            for i in xrange((len(row) - 1) / 2):
                prep_map[preposition].add((row[i * 2 + 1], int(row[i * 2 + 2])))

    return prep_map
