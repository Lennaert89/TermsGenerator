
# Terms Generator

## What This Is

Terms Generator is a Python program designed to extract specific terms and their definitions from input files (PDF, DOCX, TXT). It cross-references these terms against dictionaries provided in JSON or CSV format and generates an output file containing the matched terms and their definitions in a specified format (DOCX, HTML, or TXT).

Useful for when you have to create a list of terms used for a document, you can easily make and use custom dictionaries!

## Acknowledgments
I would like to thank [CyberVeilig Nederland](https://cyberveilignederland.nl/) for creating the cybersecurity dictionary that helped inspire this project.

## Install Instructions

### Prerequisites

- Python 3.6 or higher

### Setup

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Lennaert89/TermsGenerator.git
   cd TermsGenerator
   ```

2. **Create a virtual environment:**
   ```sh
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```sh
   pip install -r requirements.txt
   ```

## How to Use It

### Command Line Usage

The program can be run from the command line with the following syntax:

```sh
python term_extractor.py <input_file> <dict_files> [--output_format <format>] [--output_file <output>] [--log <log_file>] [--verbosity <level>] [--language <lang>]
```

### Arguments

- `input_path`: The input file to scan (DOCX, PDF, TXT) or a directory to recursively scan.
- `dict_paths`: One or more dictionary files to use (CSV, JSON), or a directory in which all .json and .csv files will be used as dictionaries.
- `--interactive`: Run the program in interactive mode.
- `--output_format`: The output format (`docx`, `html`, `txt`, `md`). Default is `docx`.
- `--output_file`: The output file name. If not specified, defaults to `output.<format>`.
- `--log`: The log file to write to. If not specified, logs will only be printed to the terminal.
- `--verbosity`: The verbosity level of logging. Default is `INFO`.
- `--language`: The language for the 'Also see' text (`en` for English, `nl` for Dutch). Default is `en`.

### Interactive Mode
To use the interactive mode, run the script with the --interactive flag:

```sh
python term_extractor.py --interactive
```

You will be prompted to enter the required inputs interactively.

### Example Commands
- For a PDF input file and JSON dictionary file, with output in DOCX format:
```sh
python term_extractor.py input.pdf dictionary.json --output_format docx --output_file output.docx --verbosity DEBUG
```
- For a DOCX input file and CSV dictionary file, with output in HTML format:
```sh
python term_extractor.py input.docx dictionary.csv --output_format html --output_file output.html --log my_log_file.log --verbosity INFO
```
- For a TXT input file and multiple dictionary files, with output in TXT format:
```sh
python term_extractor.py input.txt dictionary1.json dictionary2.csv --output_format txt --output_file output.txt --verbosity WARNING
```
- For a PDF input file and JSON dictionary file, with output in DOCX format and Dutch language for references:
```sh
python TermExtractor.py input.pdf dictionary.json --output_format docx --output_file output.docx --language nl
```

## Creating Custom Dictionaries

### JSON Format

Create a JSON file with an array of dictionaries, each containing the fields `word`, `meaning`, and `reference`. For example:

```json
[
  {
    "word": "Access Control List (ACL)",
    "meaning": "A list specifying who can access and perform operations on a resource.",
    "reference": "Authorization, Permissions"
  },
  {
    "word": "Account hijacking",
    "meaning": "The act of gaining unauthorized access to someone else's account.",
    "reference": "Identity theft, Phishing"
  }
]
```

### CSV Format

Create a CSV file with columns `word`, `meaning`, and `reference`. For example:

```csv
word,meaning,reference
Access Control List (ACL),A list specifying who can access and perform operations on a resource,Authorization
Account hijacking,The act of gaining unauthorized access to someone else's account,Identity theft
```

Feel free to customize the dictionaries with your own terms and definitions. Enjoy using Terms Generator!
