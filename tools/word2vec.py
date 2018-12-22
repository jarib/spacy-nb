#!/usr/bin/env python

"""
Based on:

    https://github.com/explosion/spacy-dev-resources/blob/master/training/word_vectors.py

"""

from __future__ import print_function, unicode_literals, division
import io
import bz2
import logging
from os import path
import os
import random
from collections import defaultdict
from pathlib import Path

import plac
import ujson as json
from gensim.models import Word2Vec
from preshed.counter import PreshCounter
import spacy

logger = logging.getLogger(__name__)

class Corpus(object):
    def __init__(self, directory):
        self.directory = directory
        self.counts = PreshCounter()

    def count_doc(self, doc):
        for word in doc:
            self.counts.inc(word.orth, 1)

    def contents(self):
        for text_loc in self.directory.rglob('*.txt'):
            with io.open(text_loc, 'r', encoding='utf8') as file_:
                text = file_.read()

            yield text

    def __iter__(self):
        for text in self.contents():
            for line in text.split("\n"):
                yield line

@plac.annotations(
    in_dir=("Location of input directory with .txt files"),
    out_loc=("Location of output file"),
    lang=("ISO language code", "option", "l", str),
    n_workers=("Number of workers", "option", "n", int),
    size=("Dimension of the word vectors", "option", "d", int),
    window=("Context window size", "option", "w", int),
    min_count=("Min count", "option", "m", int),
    negative=("Number of negative samples", "option", "g", int),
    nr_iter=("Number of iterations", "option", "i", int),
)
def main(in_dir, out_loc, lang="nb", negative=5, n_workers=4, window=5, size=128, min_count=10, nr_iter=2):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    in_dir = Path(in_dir)
    out_loc = Path(out_loc)

    if not out_loc.parent.exists():
        raise ValueError("dir of output path does not exist {}".format(out_loc.parent))

    model = Word2Vec(
        size=size,
        window=window,
        min_count=min_count,
        workers=n_workers,
        sample=1e-5,
        negative=negative
    )

    nlp = spacy.blank(lang)

    total_words = 0
    total_sents = 0

    corpus = Corpus(in_dir)

    for text_no, text in enumerate(corpus.contents()):
        total_sents += text.count('\n')

        doc = nlp(text)
        total_words += len(doc)
        corpus.count_doc(doc)

        if text_no % 50 == 0:
            logger.info("PROGRESS: at batch #%i, processed %i words", text_no, total_words)

    model.iter = nr_iter
    model.corpus_count = total_sents

    raw_vocab = defaultdict(int)

    for orth, freq in corpus.counts:
        if freq >= min_count:
            raw_vocab[nlp.vocab.strings[orth]] = freq

    model.build_vocab_from_freq(raw_vocab)
    model.train(corpus, epochs=nr_iter, total_words=total_words)

    gensim_out = str(out_loc.with_suffix('.bin'))
    word2vec_out = str(out_loc)

    model.save(gensim_out)
    model.wv.save_word2vec_format(word2vec_out)

    print('Wrote: gensim={}, word2vec={}'.format(gensim_out, word2vec_out))


if __name__ == '__main__':
    plac.call(main)