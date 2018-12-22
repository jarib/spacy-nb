# spacy-nb

Build an `nb` model for [spacy](https://spacy.io).

## Download

- [Norwegian News Corpus][NNC]

## Usage

Download and convert UD/NER data

    $ ./tools/norne.sh

Download and extract [NNC] 2012-2014

    $ ./tools/download.nnc.sh

Convert XML files to plain text:

    $ python -m tools.nnc2txt data/nnc

Build and save word frequencies

    $ python -m tools.word_freq data/nnc data/nnc.freqs.txt

Build and save word vectors

    $ python -m tools.word2vec data/nnc data/nnc.vectors.txt

Init model

    $ python -m spacy init-model nb data/nb-base data/nnc.freqs.txt --vectors-loc data/nnc.vectors.txt

Train tagger/parser

    $ mkdir data/training
    $ python -m spacy train nb data/training \
        data/norne-spacy/ud/nob/no-ud-train-ner.json \
        data/norne-spacy/ud/nob/no-ud-dev-ner.json \
        --vectors data/nb-base \
        --n-iter 30 \
        --gold-preproc \
        --gpu-id 1


[NNC](https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-4&lang=en)