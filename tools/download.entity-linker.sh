#!/bin/bash

OUTPUT_DIR="data/entity-linking"

ENTITIES_URL="https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2"
ARTICLES_URL="https://dumps.wikimedia.org/nowiki/latest/nowiki-latest-pages-articles-multistream.xml.bz2"

ENTITIES_FILE="$OUTPUT_DIR/entities.json.bz2"
ARTICLES_FILE="$OUTPUT_DIR/articles.xml.bz2"
SPACY_DIR="$OUTPUT_DIR/spacy"

mkdir -p "$OUTPUT_DIR"

[[ -f "$ENTITIES_FILE" ]] || curl -L "$ENTITIES_URL" -o "$ENTITIES_FILE"
[[ -f "$ARTICLES_FILE" ]] || curl -L "$ARTICLES_URL" -o "$ARTICLES_FILE"

git clone https://github.com/explosion/spaCy "$SPACY_DIR"
cd "$SPACY_DIR"
git checkout 10d88b09bb6afbc6653a10d192ff6f2a7abe5803



