#!/bin/bash

set -e
set -x

OUTPUT_DIR="data/norne-spacy/ud/nob"
CHECKOUT_DIR="data/norne"

mkdir -p "$OUTPUT_DIR"

[[ -d "$CHECKOUT_DIR" ]] || git clone git@github.com:ltgoslo/norne.git "$CHECKOUT_DIR"

for f in "$CHECKOUT_DIR"/ud/nob/*.conllu; do
    python -m spacy convert "$f" "$OUTPUT_DIR" -n 10 --converter conllu --morphology
done

