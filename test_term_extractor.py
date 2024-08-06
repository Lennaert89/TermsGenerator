import unittest
import os
import json
import csv
import tempfile
from term_extractor import read_input_file, load_dictionaries, find_terms_in_text, save_to_docx, save_to_html, save_to_txt, save_to_md

class TestTermExtractor(unittest.TestCase):

    def setUp(self):
        # Setup temporary directory for testing output files
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        # Cleanup temporary directory
        self.test_dir.cleanup()

    def test_read_input_file_txt(self):
        content = "This is a test document."
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
            temp_file.write(content.encode('utf-8'))
            temp_file_path = temp_file.name

        result = read_input_file(temp_file_path)
        self.assertEqual(result, content)

    def test_read_input_file_md(self):
        content = "# This is a test markdown document."
        with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as temp_file:
            temp_file.write(content.encode('utf-8'))
            temp_file_path = temp_file.name

        result = read_input_file(temp_file_path)
        self.assertEqual(result, content)

    def test_load_dictionaries_json(self):
        dict_content = [{"word": "test", "meaning": "A test term.", "reference": "sample"}]
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
            json.dump(dict_content, temp_file)
            temp_file_path = temp_file.name

        result = load_dictionaries([temp_file_path])
        self.assertIn("test", result)
        self.assertEqual(result["test"]["meaning"], "A test term.")
        self.assertEqual(result["test"]["reference"], "sample")

    def test_load_dictionaries_csv(self):
        dict_content = "word,meaning,reference\ntest,A test term.,sample\n"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
            temp_file.write(dict_content.encode('utf-8'))
            temp_file_path = temp_file.name

        result = load_dictionaries([temp_file_path])
        self.assertIn("test", result)
        self.assertEqual(result["test"]["meaning"], "A test term.")
        self.assertEqual(result["test"]["reference"], "sample")

    def test_find_terms_in_text(self):
        terms_dict = {"test": {"meaning": "A test term.", "reference": "sample"}}
        text = "This is a test document."
        result = find_terms_in_text(text, terms_dict)
        self.assertIn("test", result)
        self.assertEqual(result["test"]["meaning"], "A test term.")
        self.assertEqual(result["test"]["reference"], "sample")

    def test_save_to_docx(self):
        terms = {"test": {"meaning": "A test term.", "reference": "sample"}}
        output_path = os.path.join(self.test_dir.name, "output.docx")
        save_to_docx(terms, output_path, "Also see:")
        self.assertTrue(os.path.exists(output_path))

    def test_save_to_html(self):
        terms = {"test": {"meaning": "A test term.", "reference": "sample"}}
        output_path = os.path.join(self.test_dir.name, "output.html")
        save_to_html(terms, output_path, "Also see:")
        self.assertTrue(os.path.exists(output_path))

    def test_save_to_txt(self):
        terms = {"test": {"meaning": "A test term.", "reference": "sample"}}
        output_path = os.path.join(self.test_dir.name, "output.txt")
        save_to_txt(terms, output_path, "Also see:")
        self.assertTrue(os.path.exists(output_path))

    def test_save_to_md(self):
        terms = {"test": {"meaning": "A test term.", "reference": "sample"}}
        output_path = os.path.join(self.test_dir.name, "output.md")
        save_to_md(terms, output_path, "Also see:")
        self.assertTrue(os.path.exists(output_path))

if __name__ == '__main__':
    unittest.main()
