import spacy
import plac
import numpy
from scipy import spatial
from tqdm import tqdm
from spacy.vectors import Vectors

cosine_similarity = lambda x, y: 1 - spatial.distance.cosine(x, y)


def add_vectors(nlp, vectors_loc):
    with open(vectors_loc, "r") as f:
        shape = tuple(int(size) for size in next(f).split())

        vectors_data = numpy.zeros(shape=shape, dtype="f")
        vectors_keys = []

        for i, line in enumerate(tqdm(f)):
            line = line.rstrip()
            pieces = line.rsplit(" ", vectors_data.shape[1])
            word = pieces.pop(0)
            if len(pieces) != vectors_data.shape[1]:
                raise ValueError("invalid vectors format")
            vectors_data[i] = numpy.asarray(pieces, dtype="f")
            vectors_keys.append(word)

        for word in vectors_keys:
            if word not in nlp.vocab:
                lexeme = nlp.vocab[word]
                lexeme.is_oov = False

        nlp.vocab.vectors = Vectors(data=vectors_data, keys=vectors_keys)


def main(model, vector_path=None):
    nlp = spacy.load(model)

    if vector_path:
        add_vectors(nlp, vector_path)

    man = nlp.vocab["mann"].vector
    woman = nlp.vocab["kvinne"].vector
    queen = nlp.vocab["dronning"].vector
    king = nlp.vocab["konge"].vector

    res = king - man + woman
    computed_similarities = []

    for word in nlp.vocab:
        # Ignore words without vectors
        if not word.has_vector:
            continue

        similarity = cosine_similarity(res, word.vector)
        computed_similarities.append((word, similarity))

    computed_similarities = sorted(computed_similarities, key=lambda item: -item[1])
    print([w[0].text for w in computed_similarities[:10]])


if __name__ == "__main__":
    plac.call(main)
