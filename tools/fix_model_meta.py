import plac
import ujson
from pathlib import Path


def main(model_path):
    model_path = Path(model_path)

    with model_path.joinpath("meta.json").open(encoding="utf8") as f:
        meta = ujson.loads(f.read())

    with model_path.joinpath("tagger/cfg").open(encoding="utf8") as f:
        tagger_cfg = ujson.loads(f.read())

    meta["vectors"]["name"] = tagger_cfg["pretrained_vectors"]

    print(meta, tagger_cfg)

    with model_path.joinpath("meta.json").open("w", encoding="utf8") as f:
        f.write(ujson.dumps(meta))


if __name__ == "__main__":
    plac.call(main)
