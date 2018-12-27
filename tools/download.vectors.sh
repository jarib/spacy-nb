#!/bin/bash

URL="http://vectors.nlpl.eu/repository/11/100.zip"
OUT="data/vectors"

wget "$URL" -O "$OUT.zip"
unzip -d "$OUT" "$OUT.zip"