# -*- coding: utf-8 -*-

import logging
import os.path
import sys
import multiprocessing

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    wiki_text_file = 'resources/wiki.pl.text'
    model_file = 'model/wiki.pl.text.model'
    model_w2v_format = 'model/wiki.pl.text.vector'

    model = Word2Vec(LineSentence(wiki_text_file), size=400, window=5, min_count=5,
                     workers=multiprocessing.cpu_count())

    model.save(model_file)
    model.save_word2vec_format(model_w2v_format, binary=False)
