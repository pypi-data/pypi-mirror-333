# aitokencount

A Python utility for counting AI tokens in all files within a folder and its subfolders using OpenAI's tiktoken library with the cl100k_base encoding.

[![PyPI version](https://badge.fury.io/py/aitokencount.svg)](https://badge.fury.io/py/aitokencount)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- Recursively processes all files in a directory and its subdirectories
- Automatically skips `.git` folders to avoid processing repository metadata
- Respects `.gitignore` files if present, skipping ignored files and directories
- Uses the cl100k_base encoding by default (same encoding used by models like GPT-4 and GPT-3.5-Turbo)
- Estimates costs for processing the tokens with different AI models (GPT-4o, Claude 3.7 Sonnet, etc.)
- Provides a summary of total tokens and processed files
- Handles errors gracefully

## Installation

### From PyPI (Recommended)

```bash
pip install aitokencount
```

### From Source

1. Clone this repository or download the files
2. Set up a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

3. Install the package in development mode:

```bash
pip install -e .
```

## Usage

### Command Line

```bash
aitokencount /path/to/folder
```

Optional arguments:

```bash
# Specify a different encoding
aitokencount /path/to/folder --encoding cl100k_base

# Ignore .gitignore patterns even if a .gitignore file exists
aitokencount /path/to/folder --ignore-gitignore

# Suppress progress output, only show summary
aitokencount /path/to/folder --quiet
```

### Python API

```python
from aitokencount.core import count_tokens_in_folder

# Count tokens in a folder
results = count_tokens_in_folder('/path/to/folder', encoding_name='cl100k_base')

# Access the results
print(f"Total tokens: {results['total_tokens']}")
print(f"Files processed: {results['processed_files']}")

# Access cost estimates
for model, cost in results['cost_estimates'].items():
    print(f"Cost for {model}: ${cost:.4f}")
```

### Cost Estimation

The tool provides cost estimates for processing the tokens with different AI models:

| Model | Price per Million Tokens |
|-------|-------------------------:|
| GPT-4o | $10.00 |
| Claude 3.7 Sonnet | $15.00 |

These estimates help you understand the potential cost of processing your content with various AI models.

## Example

```bash
python token_counter.py ./my_project
```

Output:
```
Counting tokens in /absolute/path/to/my_project using cl100k_base encoding...
Found .gitignore with 5 patterns. Will ignore matching files.
Skipping .git directory: /absolute/path/to/my_project/.git
Ignored (gitignore): /absolute/path/to/my_project/node_modules/package.json
Processed: /absolute/path/to/my_project/file1.txt - 150 tokens
Processed: /absolute/path/to/my_project/file2.py - 320 tokens
...

Summary:
Total tokens: 1250
Files processed: 15
Files with errors: 2
Files skipped (gitignore): 8
Files skipped (.git): 42

Estimated costs:
  gpt-4o: $0.0125
  claude-3-7-sonnet: $0.0188
```

## Notes

- The script attempts to read all files as text files. Binary files or files with encoding issues may be skipped.
- The token count is based on the specified tiktoken encoding (cl100k_base by default).
- `.git` directories are automatically skipped to avoid processing repository metadata.
- If a `.gitignore` file exists in the target directory, the script will automatically respect its patterns and skip ignored files and directories.

## Requirements

- Python 3.6+
- tiktoken library
