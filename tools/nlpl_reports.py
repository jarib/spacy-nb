#!/usr/bin/env python

import plac
import requests
import ujson

import subprocess
import sys
import shutil

from pathlib import Path


def print_accuracy(scores, header=True):
    if header:
        print(
            "{:<7}{:<7}{:<7}{:<7}{:<7}{:<7}".format(
                "UAS", "NER P.", "NER R.", "NER F.", "Tag %", "Token %"
            )
        )

    strings = [
        "{:.3f}".format(scores["uas"]),
        "{:.3f}".format(scores["ents_p"]),
        "{:.3f}".format(scores["ents_r"]),
        "{:.3f}".format(scores["ents_f"]),
        "{:.3f}".format(scores["tags_acc"]),
        "{:.3f}".format(scores["token_acc"]),
    ]

    print(" ".join(strings))


@plac.annotations(output_dir=("Output dir for models", "positional"))
def main(output_dir):
    output_dir = Path(output_dir)

    reports = []

    for report in output_dir.glob("*/report.json"):
        with report.open() as f:
            reports.append(ujson.loads(f.read()))

    for report in reports:
        vec = report["vectors"]
        corp_desc = []

        for corp in vec["corpus"]:
            corp_desc.append(
                "{} (lemmatized={}, case preserved={}, tokens={})".format(
                    corp["description"],
                    corp["lemmatized"],
                    corp["case preserved"],
                    corp["tokens"],
                )
            )

        print()
        print("Vectors")
        print("-------")

        print("\tAlgorithm: {}".format(vec["algorithm"]["name"]))
        print("\tCorpus   : {}".format(", ".join(corp_desc)))
        print(
            "\tVectors  : dimensions={}, iterations={}, vocab size={}".format(
                vec["dimensions"], vec["iterations"], vec["vocabulary size"]
            )
        )

        print()
        print("Training")
        print("--------")

        for (idx, training) in enumerate(report["training"]):
            if "accuracy" in training:
                print_accuracy(training["accuracy"], header=idx == 0)

        print()
        print("Best model")
        print("----------")

        print_accuracy(report["best"]["accuracy"])

        print("-" * 42)


if __name__ == "__main__":
    plac.call(main)
