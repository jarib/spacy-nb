"""
    Count words from a list of .txt files

    Based on:

        https://github.com/explosion/spacy-dev-resources/blob/master/training/word_freqs.py
"""

from __future__ import unicode_literals, print_function

import plac
import io
import spacy

from spacy.lang.nb import Norwegian

from spacy.strings import StringStore
from spacy.attrs import ORTH
from spacy.tokenizer import Tokenizer
from spacy.vocab import Vocab
import spacy.util

from pathlib import Path

from preshed.counter import PreshCounter
from joblib import Parallel, delayed
from pathlib import Path
import multiprocessing

from tqdm import tqdm


def parallelize(func, iterator, n_jobs):
    Parallel(n_jobs=n_jobs)(delayed(func)(*item) for item in iterator)


def count_freqs(input_loc, output_loc):
    print("{} => {}".format(input_loc, output_loc))

    tokenizer = Norwegian.Defaults.create_tokenizer()
    counts = PreshCounter()

    with open(input_loc, "r") as file:
        for line in file:
            doc = tokenizer(line.strip())
            doc.count_by(ORTH, counts=counts)

    with open(output_loc, "w", encoding="utf8") as file_:
        for orth, freq in counts:
            string = tokenizer.vocab.strings[orth]
            if not string.isspace():
                file_.write("%d\t%s\n" % (freq, string))


def merge_counts(locs, out_loc):
    string_map = StringStore()
    counts = PreshCounter()
    df_counts = PreshCounter()

    for loc in tqdm(locs):
        with io.open(loc, "r", encoding="utf8") as file_:
            for line in file_:
                freq, word = line.strip().split("\t", 1)
                orth = string_map.add(word)
                counts.inc(orth, int(freq))
                df_counts.inc(orth, 1)

    with io.open(out_loc, "w", encoding="utf8") as file_:
        for orth, freq in counts:
            word = string_map[orth]
            file_.write("{}\t{}\t{}\n".format(freq, df_counts[orth], repr(word)))


@plac.annotations(
    input_dir=("Dir with .txt files to analyze", "positional"),
    result_path=("File to write frequencies", "positional"),
    skip_existing=("Skip file if it already exists", "option", "s", bool),
    n_jobs=("Number of workers", "option", "n", int),
)
def main(
    input_dir, result_path, skip_existing=True, n_jobs=multiprocessing.cpu_count()
):
    tasks = []
    outputs = []

    input_dir = Path(input_dir)

    for input_path in input_dir.rglob("*.txt"):
        output_path = input_path.with_suffix(".freq")
        outputs.append(output_path)

        if not skip_existing or not output_path.exists():
            tasks.append((input_path, output_path))

    if tasks:
        parallelize(count_freqs, tasks, n_jobs)

    print("Merging result to {}".format(result_path))
    merge_counts(outputs, result_path)


if __name__ == "__main__":
    plac.call(main)
