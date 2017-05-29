# coding: utf-8

import io
import re
import string

from collections import defaultdict, Counter

from PlpWrapper import PlpWrapper, GrammarCase

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


def prepositions(sentences):
    result = defaultdict(set)

    for sentence in sentences:
        words = sentence.strip().split(' ')

        word_index = 0
        words_len = len(words)
        while word_index < words_len:
            word = words[word_index]
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

    return result
