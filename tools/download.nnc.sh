#!/bin/bash

OUT="data/nnc"

mkdir -p "$OUT"

# We want non-tokenized files, which appears to be only these three years of XML

sources=(
    https://www.nb.no/sbfil/tekst/nak_2012.tar 
    https://www.nb.no/sbfil/tekst/nak_2013.tar
    https://www.nb.no/sbfil/tekst/nak_2014.tar
)

for s in "${sources[@]}"; do
    name=$(basename "$s" )
    dest="$OUT/$name"

    [[ -f "$dest" ]] || curl -L "$s" -o "$dest"
done

cd "$OUT" || exit

for f in *.tar; do
    echo "Extracting $f"
    tar xf "$f"
done

for f in **/*.tar.gz; do
    echo "Extracting $f"
    tar zxf "$f"
done

