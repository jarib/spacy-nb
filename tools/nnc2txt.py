"""
Extract plain text from an XML file in the Norwegian News Corpus.
"""

import plac
from bs4 import BeautifulSoup
import glob
from pathlib import Path


def main(directory = '.'):
    files = glob.glob(directory + "/**/*.xml")

    for xml_file in files:
        xml_file = Path(xml_file)

        print(xml_file)

        with open(xml_file) as file:
            soup = BeautifulSoup(file, "lxml-xml")
            text = [p.text for p in soup("p")]

        with open(xml_file.with_suffix('.txt'), 'w') as f:
            f.write("\n".join(text))



if __name__ == "__main__":
    plac.call(main)
