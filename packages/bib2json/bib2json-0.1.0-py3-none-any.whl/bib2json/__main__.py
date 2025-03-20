#!/usr/bin/env python3
"""
Command-line interface for bib2json
"""

import argparse
import sys
import os
from .converter import convert_file


def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(description="BibTeX to JSON Converter")
    parser.add_argument("-i", "--input", required=True, help="Input BibTeX file")
    parser.add_argument("-o", "--output", help="Output JSON file (optional)")
    parser.add_argument(
        "--include_bibtex",
        action="store_true",
        help="Include BibTeX field in the JSON output",
    )

    args = parser.parse_args()
    
    # If no output file is specified, create one based on the input file
    output_file = args.output
    if output_file is None:
        # Get the filename without extension and add .json
        base_name = os.path.splitext(os.path.basename(args.input))[0]
        output_file = f"{base_name}.json"

    try:
        convert_file(args.input, output_file, args.include_bibtex)
        print(
            f"The BibTeX input file '{args.input}' "
            f"has been converted to '{output_file}'"
        )
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())