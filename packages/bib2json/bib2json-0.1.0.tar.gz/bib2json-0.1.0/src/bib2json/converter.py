"""
Core functionality for converting BibTeX to JSON
"""

import json
import bibtexparser
from typing import Dict, List, Optional, Union, TextIO


def json_to_bibtex(entry: Dict) -> str:
    """
    Convert a BibTeX entry (as dict) back to BibTeX format

    Args:
        entry: Dictionary containing a BibTeX entry

    Returns:
        String representation of the BibTeX entry
    """
    bibtex = f"@{entry['ENTRYTYPE']}{{{entry['ID']},\n"
    for key, value in entry.items():
        if key not in ["ENTRYTYPE", "ID"]:
            bibtex += f"    {key} = {{{value}}},\n"
    bibtex = bibtex.rstrip(",\n") + "\n}\n\n"
    return bibtex


def convert_string(bibtex_content: str, include_bibtex: bool = False) -> List[Dict]:
    """
    Convert BibTeX content string to a list of entry dictionaries

    Args:
        bibtex_content: String containing BibTeX entries
        include_bibtex: Whether to include the original BibTeX in the output

    Returns:
        List of dictionaries, each representing a BibTeX entry
    """
    bib_database = bibtexparser.loads(bibtex_content)
    
    if include_bibtex:
        for entry in bib_database.entries:
            entry["bibtex"] = json_to_bibtex(entry)
    
    return bib_database.entries


def convert_file(
    bibtex_input: Union[str, TextIO],
    json_output: Union[str, TextIO],
    include_bibtex: bool = False,
) -> None:
    """
    Convert a BibTeX file to JSON

    Args:
        bibtex_input: Input BibTeX filename or file object
        json_output: Output JSON filename or file object
        include_bibtex: Whether to include the original BibTeX in the output

    Returns:
        None
    """
    # Handle string filenames or file objects
    if isinstance(bibtex_input, str):
        with open(bibtex_input, "r", encoding="utf-8") as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
    else:
        bib_database = bibtexparser.load(bibtex_input)

    # Add BibTeX field to each JSON entry if requested
    if include_bibtex:
        for entry in bib_database.entries:
            entry["bibtex"] = json_to_bibtex(entry)

    # Write the JSON file
    if isinstance(json_output, str):
        with open(json_output, "w", encoding="utf-8") as json_file:
            json.dump(bib_database.entries, json_file, indent=4)
    else:
        json.dump(bib_database.entries, json_output, indent=4)