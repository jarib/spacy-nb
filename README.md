# spacy-nb

Build a [spacy](https://spacy.io) model for `nb` (Norwegian Bokmål).

## Usage

Download and convert UD/NER data

    ./tools/download.norne.sh

Download and extract [Norwegian News Corpus][nnc] data (2012-2014 subset)

    ./tools/download.nnc.sh

Convert XML files to plain text, but ignore paths that match 'nno' ("new norwegian"):

    python -m tools.nnc2txt data/nnc --ignore '*nno*'

Create word frequencies

    python -m tools.word_freq data/nnc data/nnc.freqs.txt

Create word vectors

    python -m tools.word2vec data/nnc data/nnc.vectors.txt

Init model

    python -m spacy init-model nb data/nb-base data/nnc.freqs.txt --vectors-loc data/nnc.vectors.txt

Train tagger/parser

    mkdir data/training

    python -m spacy train nb data/training \
        data/norne-spacy/ud/nob/no-ud-train-ner.json \
        data/norne-spacy/ud/nob/no-ud-dev-ner.json \
        --vectors data/nb-base \
        --n-iter 30 \
        --gold-preproc \
        --use-gpu 1


## Links

* [Norwegian News Corpus][nnc]
* [Universal Dependencies for Bokmål](https://github.com/UniversalDependencies/UD_Norwegian-Bokmaal)
* [ltgoslo/norne](https://github.com/ltgoslo/norne) - NER on top of UD

[nnc]: https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-4&lang=en