# Email Extractor

> A professional Python console application that extracts, validates, and saves email addresses from text files.

Reads mixed content from `input.txt`, finds email-like strings with regular expressions, removes duplicates, validates each entry, and writes clean results to `output.txt`.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Example Output](#example-output)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Project Overview

The Email Extractor processes unstructured text and pulls out email addresses embedded in paragraphs, lists, or contact exports. Each candidate match is validated with strict rules, invalid tokens are discarded, duplicates are removed, and the remaining addresses are sorted alphabetically before being saved.

The application is built with Python 3.11+ and uses only the standard library. It reports extraction statistics and execution time in a clear console summary.

---

## Features

| Feature | Description |
| --- | --- |
| File input | Reads source text from `input.txt` |
| Regex extraction | Finds email-like patterns in free-form text |
| Validation | Rejects malformed addresses (double dots, missing parts, bad TLDs) |
| Deduplication | Removes duplicate emails (case-insensitive) |
| Alphabetical sort | Outputs valid emails in sorted order |
| File output | Saves results to `output.txt` (one email per line) |
| Statistics | Reports total found, unique valid, and invalid ignored |
| Execution time | Displays runtime in seconds |
| Error handling | Graceful messages for missing or unreadable files |
| Clear output | Structured console sections and summary |

---

## Folder Structure

```text
Task-3-EmailExtractor/
├── main.py       # Application source code
├── input.txt     # Sample input with mixed valid/invalid emails
├── output.txt    # Generated valid emails (created on run)
└── README.md     # Project documentation
```

---

## Installation

1. Clone or download this repository.
2. Open a terminal and navigate to the project folder:

   ```bash
   cd Task-3-EmailExtractor
   ```

3. Confirm Python 3.11 or newer is installed:

   ```bash
   python --version
   ```

No additional packages are required.

---

## Usage

Place your source text in `input.txt`, then run:

```bash
python main.py
```

Or from the repository root:

```bash
python Task-3-EmailExtractor\main.py
```

After execution, valid emails appear in `output.txt` and a summary is printed to the console.

### Custom Input

Replace the contents of `input.txt` with your own text. The extractor scans the entire file and finds all email-like patterns automatically.

---

## Example Output

```text
========================================================================
                            EMAIL EXTRACTOR
========================================================================

Files
-----
  Input : C:\...\Task-3-EmailExtractor\input.txt
  Output: C:\...\Task-3-EmailExtractor\output.txt

Extraction Summary
------------------
  Total emails found     : 36
  Unique valid emails    : 29
  Invalid entries ignored: 4
  Duplicates removed     : 3
  Execution time         : 0.0007 seconds

Valid Emails
------------
  admin@open-source.software
  alice.johnson@example.com
  analytics@datacorp.ai
  bob.smith@company.org
  ...

Saved 29 email(s) to 'output.txt'.

Email extraction completed successfully.
```

---

## Future Improvements

- Command-line arguments for custom input/output file paths
- Export results to CSV or JSON format
- Batch processing of multiple input files
- Configurable validation strictness levels
- Highlight line numbers where each email was found
- Unit tests for regex and validation logic
- Optional DNS/MX record verification for domains

---

## License

This project is part of the CodeAlpha Python internship tasks and is provided for educational purposes. Feel free to use, modify, and distribute with attribution.
