import unittest
import os
import json
import csv
import tempfile
import shutil
from term_extractor import read_input_file, load_dictionaries, find_terms_in_text, save_terms, main

class TestTermExtractor(unittest.TestCase):

    def setUp(self):
        # Setup temporary directory for testing output files
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_dict_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        # Cleanup temporary directory
        self.test_dir.cleanup()
        self.test_dict_dir.cleanup()

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
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w', encoding='utf-8') as temp_file:
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

    def test_save_terms_docx(self):
        terms = {"test": {"meaning": "A test term.", "reference": "sample"}}
        output_path = os.path.join(self.test_dir.name, "output.docx")
        save_terms(terms, output_path, "Also see:", output_format='docx')
        self.assertTrue(os.path.exists(output_path))

    def test_save_terms_html(self):
        terms = {"test": {"meaning": "A test term.", "reference": "sample"}}
        output_path = os.path.join(self.test_dir.name, "output.html")
        save_terms(terms, output_path, "Also see:", output_format='html')
        self.assertTrue(os.path.exists(output_path))

    def test_save_terms_txt(self):
        terms = {"test": {"meaning": "A test term.", "reference": "sample"}}
        output_path = os.path.join(self.test_dir.name, "output.txt")
        save_terms(terms, output_path, "Also see:", output_format='txt')
        self.assertTrue(os.path.exists(output_path))

    def test_save_terms_md(self):
        terms = {"test": {"meaning": "A test term.", "reference": "sample"}}
        output_path = os.path.join(self.test_dir.name, "output.md")
        save_terms(terms, output_path, "Also see:", output_format='md')
        self.assertTrue(os.path.exists(output_path))

    def test_recursive_load_dictionaries(self):
        dict_content_json = [{"word": "test_json", "meaning": "A test term from json.", "reference": "sample_json"}]
        dict_content_csv = "word,meaning,reference\ntest_csv,A test term from csv.,sample_csv\n"

        os.makedirs(os.path.join(self.test_dict_dir.name, "subdir"), exist_ok=True)
        with open(os.path.join(self.test_dict_dir.name, "subdir", "dict.json"), 'w', encoding='utf-8') as json_file:
            json.dump(dict_content_json, json_file)
        with open(os.path.join(self.test_dict_dir.name, "subdir", "dict.csv"), 'w', encoding='utf-8') as csv_file:
            csv_file.write(dict_content_csv)

        result = load_dictionaries([self.test_dict_dir.name])
        self.assertIn("test_json", result)
        self.assertEqual(result["test_json"]["meaning"], "A test term from json.")
        self.assertIn("test_csv", result)
        self.assertEqual(result["test_csv"]["meaning"], "A test term from csv.")

    def test_recursive_process_files(self):
        input_content = "This is a test document with a test_json term."
        dict_content_json = [{"word": "test_json", "meaning": "A test term from json.", "reference": "sample_json"}]

        os.makedirs(os.path.join(self.test_dir.name, "input_subdir"), exist_ok=True)
        with open(os.path.join(self.test_dir.name, "input_subdir", "input.txt"), 'w', encoding='utf-8') as input_file:
            input_file.write(input_content)

        os.makedirs(os.path.join(self.test_dict_dir.name, "subdir"), exist_ok=True)
        with open(os.path.join(self.test_dict_dir.name, "subdir", "dict.json"), 'w', encoding='utf-8') as json_file:
            json.dump(dict_content_json, json_file)

        output_file = os.path.join(self.test_dir.name, "output.txt")
        main(self.test_dir.name, [self.test_dict_dir.name], output_format='txt', output_file=output_file, log_file=None, verbosity='INFO', language='en')

        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r', encoding='utf-8') as output_file:
            output_content = output_file.read()
            self.assertIn("test_json", output_content)
            self.assertIn("A test term from json.", output_content)

if __name__ == '__main__':
    unittest.main()
