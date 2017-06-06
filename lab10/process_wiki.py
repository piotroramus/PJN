# -*- coding: utf-8 -*-

from __future__ import print_function

import logging
import os.path
import six
import sys

from gensim.corpora import WikiCorpus

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    wiki_archive_file = 'resources/plwiki-latest-pages-articles3.xml.bz2'
    wiki_text_file = 'resources/wiki.pl.text'

    with open(wiki_text_file) as output:
        wiki = WikiCorpus(wiki_archive_file, lemmatize=False, dictionary={})
        i = 0
        for text in wiki.get_texts():
            if six.PY3:
                output.write(b' '.join(text).decode('utf-8') + '\n')
            else:
                output.write(" ".join(text) + "\n")
            i += 1
            if i % 10000 == 0:
                logger.info("Saved {} articles".format(i))

    logger.info("Finished saving {} articles".format(i))
