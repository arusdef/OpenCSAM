#!/usr/bin/env python3
"""This script converts PDF files to plain text."""

from pathlib import Path
import tika
from tika import parser
import json

def main():
    # Input location of the pdf documents.
    in_dir = Path("documents")

    # Output directory to store the parsed files with plain text.
    out_dir = Path("plaintext")
    out_dir.mkdir(parents=True, exist_ok=True)

    for in_path in in_dir.iterdir():
        if in_path.suffix == '.pdf':
            print("Parsing " + str(in_path))

            # Parse the PDF files including as plain text.
            # There is an option to get text including XML tags (xmlContent=True).
            # In principle, that might be useful for further structuring of the documents.
            # - For example, we can identify links by looking for href. However, the links can be easily detected with
            #   regular expressions.
            # - Chapter titles could be detected as single-sentence paragraphs.
            # - Other XML tags do not seem to be useful...
            # - Metadata appear at the beginning. This is a duplication because the metadata get extracted into
            #   a separate JSON field.
            parsed = parser.from_file(str(in_path))

            out_path = out_dir.joinpath(Path(in_path.stem + ".json"))
            print("Saving plain text to " + str(out_path))

            with out_path.open('w') as out_file:
                json.dump(parsed, out_file, sort_keys=True, indent=4)

if __name__ == "__main__":
    main()
