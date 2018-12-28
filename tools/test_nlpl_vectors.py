#!/usr/bin/env python

import plac
import requests
import ujson

import subprocess
import sys
import shutil

from pathlib import Path


class Model(object):
    @staticmethod
    def all(repository_id="11", language="nob", corpus_id=None, out=None):
        repo = requests.get(
            "http://vectors.nlpl.eu/repository/{}.json".format(repository_id)
        ).json()

        corpora = {}
        algorithms = {}

        for alg in repo["algorithms"]:
            algorithms[alg["id"]] = alg

        for corp in repo["corpora"]:
            corpora[corp["id"]] = corp

        filtered_corpus_ids = [
            key for key, value in corpora.items() if value["language"] == language
        ]

        models = [
            model
            for model in repo["models"]
            if model["corpus"][0] in filtered_corpus_ids
        ]

        if corpus_id:
            models = [
                m
                for m in models
                if len(m["corpus"]) == 1 and m["corpus"][0] == corpus_id
            ]

        result = []

        for model in models:
            model["repository_id"] = repository_id
            model["corpus"] = [corpora[corpus_id] for corpus_id in model["corpus"]]
            model["algorithm"] = algorithms[model["algorithm"]]

            result.append(Model(model, out=out))

        return result

    def __init__(self, attrs, out=None):
        self.attrs = attrs

        if out:
            self.out = out

    def url(self):
        return "http://vectors.nlpl.eu/repository/{}.zip".format(
            self.id().replace("-", "/")
        )

    @property
    def out(self):
        return self._out

    @out.setter
    def out(self, val):
        output_folder = Path(val)
        output_folder.mkdir(exist_ok=True)

        self._out = output_folder.joinpath(self.id())

        self.meta_path = self.out.joinpath("meta.json")
        self.model_path = self.out.joinpath("model.txt")
        self.training_path = self.out.joinpath("training")

    def fetch(self, force=False):
        zip_path = self.out.with_suffix(".zip")

        try:
            if force or not self.out.exists():
                print("downloading to {}".format(zip_path))
                res = subprocess.call(["curl", "-o", str(zip_path), self.url()])

                if res != 0:
                    raise ValueError("download failed {}".format(self.url()))

                print("unzippiing to {}".format(self.out))
                res = subprocess.call(["unzip", "-od", str(self.out), str(zip_path)])

                if res != 0:
                    raise ValueError("unzip failed {}".format(str(zip_path)))
        finally:
            if zip_path.exists():
                zip_path.unlink()

    def train(self, force=False, n_iter=15):
        vectors_model_path = self.out.joinpath("vectors")

        if force or not vectors_model_path.exists():
            shutil.rmtree(vectors_model_path, ignore_errors=True)

            cmd = [
                sys.executable,
                "-m",
                "spacy",
                "init-model",
                "nb",
                vectors_model_path,
                "--vectors-loc",
                self.model_path,
            ]

            print("Building vectors model (spacy init-model) for {}".format(self.attrs))
            result = subprocess.run(cmd)

            if result.returncode != 0:
                raise ValueError(
                    "failed to build spacy model for {}\n".format(self.id())
                )

        if self.training_path.exists():
            if force:
                shutil.rmtree(self.training_path)
            else:
                print("Training path exists and force=False, skipping")
                return

        self.training_path.mkdir(exist_ok=True)

        # run training and collect output to a file
        cmd = [
            sys.executable,
            "-m",
            "spacy",
            "train",
            "nb",
            str(self.training_path),
            "data/norne-spacy/ud/nob/no-ud-train-ner.json",
            "data/norne-spacy/ud/nob/no-ud-dev-ner.json",
            "--vectors",
            str(vectors_model_path),
            "--n-iter",
            str(n_iter),
            "--use-gpu",
            "1",
        ]

        print("TRAINING")
        print("cmd: {}".format(" ".join(cmd)))

        result = subprocess.run(cmd)

        if result.returncode != 0:
            raise ValueError("failed to train {}".format(self.id()))

    def id(self):
        return "{}-{}".format(self.attrs["repository_id"], self.attrs["id"])

    def __str__(self):
        return "model(id={}, algo=({}), corpus=({})) lemma={}".format(
            self.id(),
            self.attrs["algorithm"]["name"],
            [c["description"] for c in self.attrs["corpus"]],
            [c["lemmatized"] for c in self.attrs["corpus"]],
        )


@plac.annotations(
    output_dir=("Dir where results will be saved", "positional"),
    model_id=("Dir where results will be saved", "option", "m", str),
    n_iter=("Number of iterations", "option", "n", int),
    force=("Overwrite existing data", "option", "f", bool),
)
def main(output_dir, model_id=None, n_iter=15, force=False):
    output_dir = Path(output_dir)

    # fmt: off
    IGNORED = [
        "11-58", # encoding issues
        "11-165", # not word2vec text
    ]
    # fmt: on

    models = Model.all(repository_id=11, language="nob", out=output_dir)

    for m in models:
        if m.id() in IGNORED:
            continue

        if model_id and model_id != m.id():
            continue

        m.fetch(force=force)
        m.train(n_iter=n_iter, force=force)


if __name__ == "__main__":
    plac.call(main)
