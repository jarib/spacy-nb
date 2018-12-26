#!/usr/bin/env python

import plac

import subprocess
import sys

from pathlib import Path
import srsly
import os

from .fix_model import fix_model


def print_accuracy(scores, header=True, indent=0):
    ind = "\t" * indent

    if header:
        print(
            "{}{:<7}{:<7}{:<7}{:<7}{:<7}{:<7}".format(
                ind, "UAS", "NER P.", "NER R.", "NER F.", "Tag %", "Token %"
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

    print(ind + " ".join(strings))


def get_size(start_path):
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)

    return total_size


@plac.annotations(
    output_dir=("Output dir for models", "positional"),
    evaluate=('Run "spacy evaluate" for each model', "flag", "e", bool),
)
def main(output_dir, evaluate=False):
    output_dir = Path(output_dir)
    reports = []

    for work_dir in output_dir.glob("*"):
        report = {"path": str(work_dir), "training": []}
        report["vectors"] = srsly.read_json(work_dir.joinpath("meta.json"))

        model_dirs = list(work_dir.joinpath("training").glob("model[0-9]*"))

        for model_dir in model_dirs:
            fix_model(model_dir)

            model = {
                "meta": srsly.read_json(model_dir.joinpath("meta.json")),
                "path": str(model_dir),
                "size": get_size(model_dir),
            }
            report["training"].append(model)

        best_dir = work_dir.joinpath("training/model-best")

        if best_dir.exists():
            fix_model(best_dir)

            report["best"] = {
                "meta": srsly.read_json(model_dir.joinpath("meta.json")),
                "path": str(best_dir),
                "size": get_size(best_dir),
            }

        reports.append(report)

    for (idx, report) in enumerate(reports):
        head = "Model {:>3}".format(idx)
        print("=" * len(head))
        print(head)
        print("=" * len(head))
        print("\tPath: {}".format(report["path"]))

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
            if "accuracy" in training["meta"]:
                print_accuracy(training["meta"]["accuracy"], header=idx == 0, indent=1)

        print()
        print("Best")
        print("----")

        if not "best" in report:
            print("\n\tNone saved.")
            return

        print("\tPath: {}".format(report["best"]["path"]))
        print("\tSize: {} MB".format(round(report["best"]["size"] / 1024 ** 2)))
        print()

        print_accuracy(report["best"]["meta"]["accuracy"], indent=1)

        if evaluate:
            print()
            print("Evaluate")
            print("--------")

            res = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "spacy",
                    "evaluate",
                    "-G",
                    "-g",
                    "1",
                    report["best"]["path"],
                    "data/norne-spacy/ud/nob/no-ud-test-ner.json",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf8",
            )

            if res.returncode != 0:
                print("Evaluation failed!")
                print(res.stderr)

            for line in res.stdout.split("\n"):
                if not "===" in line:
                    print("\t", line)

        print("\n")


if __name__ == "__main__":
    plac.call(main)
