#!/bin/bash

set -e
set -x

COMMIT="8cd770f0514ea002e3308733639ceef0ca5f1d5c"
OUTPUT_DIR="data/norne-spacy/ud/nob"
CHECKOUT_DIR="data/norne-$COMMIT"

mkdir -p "$OUTPUT_DIR"

[[ -d "$CHECKOUT_DIR" ]] || git clone https://github.com/ltgoslo/norne "$CHECKOUT_DIR"

cd "$CHECKOUT_DIR" && git checkout "$COMMIT" && cd -

python "$CHECKOUT_DIR/scripts/ud2spacy.py" --outputdir "$OUTPUT_DIR" nob

for f in "$OUTPUT_DIR"/*.conllu; do
    python -m spacy convert "$f" "$OUTPUT_DIR" -n 10 --converter conllu --morphology --file-type json
done

