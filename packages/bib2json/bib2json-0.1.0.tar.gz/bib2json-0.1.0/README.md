# Bib2JSON

Bib2JSON is a simple Python tool for converting BibTeX files to JSON format. It maintains the structure and content of your bibliographic entries while making them accessible in a more versatile machine-readable format.

Originally created by [Brian Rabern](https://github.com/brianrabern/bib2json), this package provides a Python library and command-line interface for BibTeX to JSON conversion.

## Installation

```bash
pip install bib2json
```

## Usage

### Command Line

```bash
# Basic usage with explicit output file
bib2json input.bib output.json

# Basic usage with default output file (will create input.json)
bib2json input.bib

# Include original BibTeX in the JSON output
bib2json input.bib --include_bibtex
```

### Python API

```python
import bib2json

# Convert BibTeX to JSON
bib2json.convert_file("input.bib", "output.json")

# Include original BibTeX in the JSON output
bib2json.convert_file("input.bib", "output.json", include_bibtex=True)
```

## Features

- Convert BibTeX files to JSON
- Option to retain the original BibTeX entries within the JSON output
- Simple command-line interface
- Programmatic API for integration with other Python code

## License

MIT