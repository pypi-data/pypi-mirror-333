"""Tests for the bib2json converter"""

import json
import os
import tempfile
import unittest
from bib2json.converter import convert_string, convert_file


class TestConverter(unittest.TestCase):
    """Test suite for the bib2json converter"""

    def setUp(self):
        self.sample_bibtex = """@article{test2023,
  author = {Test Author},
  title = {Test Title},
  journal = {Test Journal},
  year = {2023},
  volume = {1},
  pages = {1--10}
}"""

    def test_convert_string(self):
        """Test converting a BibTeX string to JSON"""
        result = convert_string(self.sample_bibtex)
        self.assertEqual(len(result), 1)
        entry = result[0]
        self.assertEqual(entry["ENTRYTYPE"], "article")
        self.assertEqual(entry["ID"], "test2023")
        self.assertEqual(entry["author"], "Test Author")
        self.assertEqual(entry["title"], "Test Title")

    def test_convert_string_with_bibtex(self):
        """Test including original BibTeX in the JSON output"""
        result = convert_string(self.sample_bibtex, include_bibtex=True)
        self.assertEqual(len(result), 1)
        entry = result[0]
        self.assertIn("bibtex", entry)
        self.assertIn("@article{test2023", entry["bibtex"])

    def test_convert_file(self):
        """Test converting a BibTeX file to a JSON file"""
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as bibtex_file:
            bibtex_file.write(self.sample_bibtex)
            bibtex_filename = bibtex_file.name

        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as json_file:
            json_filename = json_file.name

        try:
            convert_file(bibtex_filename, json_filename)
            
            with open(json_filename, "r") as f:
                result = json.load(f)
            
            self.assertEqual(len(result), 1)
            entry = result[0]
            self.assertEqual(entry["ENTRYTYPE"], "article")
            self.assertEqual(entry["ID"], "test2023")
            self.assertEqual(entry["author"], "Test Author")
            self.assertEqual(entry["title"], "Test Title")
        finally:
            # Clean up temp files
            os.unlink(bibtex_filename)
            os.unlink(json_filename)


if __name__ == "__main__":
    unittest.main()