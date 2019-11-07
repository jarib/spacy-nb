# spacy-nb

Build a [spacy](https://spacy.io) model for `nb` (Norwegian Bokmål).

## Usage

Download and convert UD/NER data

    ./tools/download.norne.sh

Download and unpack pre-trained word2vec model

    ./tools/download.vectors.sh

Create spacy model with vectors (add `--prune-vectors N` to reduce model size)

    python -m spacy init-model nb data/nb-base --vectors-loc data/vectors/model.txt

If you have a GPU, run:

    pip install -U spacy[cuda]

Train tagger/parser

    mkdir data/training

    python -m spacy train nb data/training \
        data/norne-spacy/ud/nob/no_bokmaal-ud-train.json \
        data/norne-spacy/ud/nob/no_bokmaal-ud-dev.json \
        --vectors data/nb-base \
        --n-iter 30 \
        --use-gpu 0

## Train word2vec from Norwegian News Corpus (experimental)

**This is currently not scoring well. The pre-trained vectors from NLPL works a lot better.**

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

## Entity Linking


Assuming you have a spacy model in `data/nb-lg`:

    ./tools/download.entity-linker.sh
    cd data/entity-linking/spacy/bin/wiki_entity_linking/

    python wikidata_pretrain_kb.py \
        ../../../entities.json.bz2 \
        ../../../articles.xml.bz2 \
        ../../../result \
        ../../../../nb-lg

    python wikidata_train_entity_linker.py ../../../result/

## Links

* [Norwegian News Corpus][nnc]
* [Universal Dependencies for Bokmål](https://github.com/UniversalDependencies/UD_Norwegian-Bokmaal)
* [ltgoslo/norne](https://github.com/ltgoslo/norne) - NER on top of UD
* [Pre-trained word vectors](http://vectors.nlpl.eu/repository/)

[nnc]: https://www.nb.no/sprakbanken/show?serial=oai%3Anb.no%3Asbr-4&lang=en

