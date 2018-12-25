import plac
import spacy


def main(model_path):
    nlp = spacy.load(model_path)
    doc = nlp("hund katt banan")

    for token1 in doc:
        for token2 in doc:
            print("{} <=> {} = {}".format(token1, token2, token1.similarity(token2)))


if __name__ == "__main__":
    plac.call(main)
