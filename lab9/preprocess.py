# coding: utf-8

import io
import re
from collections import defaultdict


def split_to_sentences(input_file):
    new_doc_pattern = r'#\d{6}'
    new_doc_split = re.compile(new_doc_pattern)

    sentence_pattern = r'\.\s+(?=[A-ZĆŁŚŻŹ])'
    sentence_split = re.compile(sentence_pattern)

    sentences = defaultdict(list)
    text_num = 0
    with io.open(input_file, 'r', encoding='utf-8') as f:
        documents = re.split(new_doc_split, f.read())[1:]
        for doc in documents:
            text_num += 1
            for sentence in re.split(sentence_split, doc):
                sentences[text_num].append(sentence)

    return sentences
