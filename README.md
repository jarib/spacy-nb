# spacy-nb

Build an `nb` model for [spacy](https://spacy.io).

## Download 

- [Norwegian News Corpus][NNC]

## Usage

Download and extract [NNC] (2012-2014)

    $ ./tools/download.nnc.sh

Convert XML files to plain text:

    $ python -m tools.nnc2txt data/nnc

Build and save word vectors and frequencies

    $ python -m tools.word2vec data/nnc

Init model

    $ python -m ...

Download and convert UD/NER data

    $ ./tools/norne.sh

Train tagger/parser

    $ mkdir data/models
    $ python -m spacy train nb data/models \
        data/norne-spacy/ud/nob/no-ud-train-ner.json \
        data/norne-spacy/ud/nob/no-ud-dev-ner.json \
        --n-iter 30

[NNC](https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-4&lang=en)