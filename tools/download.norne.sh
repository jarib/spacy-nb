#!/bin/bash

set -e
set -x

OUTPUT_DIR="data/norne-spacy/ud/nob"
CHECKOUT_DIR="data/norne"

mkdir -p "$OUTPUT_DIR"

[[ -d "$CHECKOUT_DIR" ]] || git clone git@github.com:ltgoslo/norne.git "$CHECKOUT_DIR"

cd $CHECKOUT_DIR && git checkout 8cd770f0514ea002e3308733639ceef0ca5f1d5c && cd -

python "$CHECKOUT_DIR/scripts/ud2spacy.py" --outputdir "$OUTPUT_DIR" nob

for f in "$OUTPUT_DIR"/*.conllu; do
    python -m spacy convert "$f" "$OUTPUT_DIR" -n 10 --converter conllu --morphology --file-type json
done

