"""

Adds vectors.name to meta.json.
See https://github.com/explosion/spaCy/issues/3093

"""

import plac
import srsly
from pathlib import Path


def main(model_path):
    model_path = Path(model_path)
    meta_path = model_path.joinpath("meta.json")

    meta = srsly.read_json(meta_path)
    tagger_cfg = srsly.read_json(model_path.joinpath("tagger/cfg"))

    meta["vectors"]["name"] = tagger_cfg["pretrained_vectors"]

    srsly.write_json(meta_path, meta)
    print('fixed')


if __name__ == "__main__":
    plac.call(main)
