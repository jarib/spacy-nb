"""
Extract plain text from an XML file in the Norwegian News Corpus.
"""

import sys
import plac
from bs4 import BeautifulSoup
from pathlib import Path
import fnmatch


@plac.annotations(
    directory=("Dir with files to process", "positional"),
    overwrite=("Overwrite existing texts", "flag", "o"),
    ignore=("Ignore files that match the given glob-style pattern", "option", "i", str),
)
def main(directory=".", overwrite=False, ignore=None):
    directory = Path(directory)

    for xml_file in directory.rglob("*.xml"):
        output_file = xml_file.with_suffix(".txt")

        if ignore and fnmatch.fnmatch(str(xml_file), ignore):
            continue

        try:
            if overwrite or not output_file.exists():
                print("{} => {}".format(xml_file, output_file))

                with open(xml_file) as file:
                    soup = BeautifulSoup(file, "lxml-xml")
                    text = [p.text for p in soup("p")]

                with open(output_file, "w") as f:
                    f.write("\n".join(text))
        except UnicodeEncodeError as e:
            print("ignoring unicode error", file=sys.stderr)


if __name__ == "__main__":
    plac.call(main)
