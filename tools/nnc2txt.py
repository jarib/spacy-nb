"""
Extract plain text from an XML file in the Norwegian News Corpus.
"""

import sys
import plac
from bs4 import BeautifulSoup
import glob
from pathlib import Path

def main(directory = '.', skip_existing=True):
    directory = Path(directory)

    for xml_file in directory.rglob('*.xml'):
        xml_file = Path(xml_file)
        output_file = xml_file.with_suffix('.txt')

        try:
            if not skip_existing or not output_file.exists():
                print(xml_file)

                with open(xml_file) as file:
                    soup = BeautifulSoup(file, "lxml-xml")
                    text = [p.text for p in soup("p")]

                with open(output_file, 'w') as f:
                    f.write("\n".join(text))
        except UnicodeEncodeError as e:
            print('ignoring unicode error', file=sys.stderr)



if __name__ == "__main__":
    plac.call(main)
