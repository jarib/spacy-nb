import plac
import spacy
from spacy import displacy

def main(model, text, output_svg_path):
    nlp = spacy.load(model)
    doc = nlp(text)

    svg = displacy.render(doc, style='dep')
    with open(output_svg_path, 'w', encoding='utf-8') as f:
        f.write(svg)

if __name__ == '__main__':
    plac.call(main)
