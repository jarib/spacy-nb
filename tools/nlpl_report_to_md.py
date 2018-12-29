#!/usr/bin/env python

import srsly
import re
import plac


def parse_evaluation(cmd_output):
    data = {}
    num_re = re.compile(r"^[\d.]+$")

    for line in cmd_output.split("\n"):
        line = line.replace("\x1b[1m", "").strip()

        if len(line) > 0 and not "===" in line:
            key, val = re.split(r"\s{2,}", line, 2)
            data[key] = float(val) if num_re.match(val) else val

    return data


@plac.annotations(input_json=("JSON file with report", "positional"))
def main(input_json):
    data = srsly.read_json(input_json)

    headers = [
        "Corpus",
        "Lemmatized",
        "Algorithm",
        "Dimensions",
        "Window",
        "Vocab size",
        "Model size",
        "TOK",
        "POS",
        "UAS",
        "LAS",
        "NER P",
        "NER R",
        "NER F",
    ]

    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join(["-" * len(h) for h in headers]) + " |")

    for row in data:
        url = "http://vectors.nlpl.eu/repository/11/{}.zip".format(row["vectors"]["id"])
        corpus_name = " + ".join([c["description"] for c in row["vectors"]["corpus"]])
        corpus_lemmatized = " ".join(
            set([str(c["lemmatized"]) for c in row["vectors"]["corpus"]])
        )

        ev = parse_evaluation(row["evaluation"])

        values = [
            "[{}]({})".format(corpus_name, url),
            corpus_lemmatized,
            row["vectors"]["algorithm"]["name"],
            str(row["vectors"]["dimensions"]),
            str(row["vectors"]["window"]),
            str(row["vectors"]["vocabulary size"]),
            "{}MB".format(round(row["best"]["size"] / 1024 ** 2)),
            str(ev["TOK"]),
            str(ev["POS"]),
            str(ev["UAS"]),
            str(ev["LAS"]),
            str(ev["NER P"]),
            str(ev["NER R"]),
            str(ev["NER F"]),
        ]

        print("| " + " | ".join(values) + " |")


if __name__ == "__main__":
    plac.call(main)
