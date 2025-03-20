# Repo Serializer

A Python utility for serializing local Git repositories into a structured text file, capturing the directory structure (in ASCII format), file names, and contents of source files. Ideal for providing a comprehensive snapshot of a repository for code review, documentation, or interaction with large language models (LLMs).

## Installation

```bash
# Install from PyPI
pip install repo-serializer
```

## Usage

### Command Line

```bash
# Basic usage
repo-serializer /path/to/repository

# Specify output file
repo-serializer /path/to/repository -o output.txt
```

### Python API

```python
from repo_serializer import serialize

# Serialize a repository
serialize("/path/to/repository", "output.txt")
```

## Features

- **Directory Structure:** Clearly visualize repository structure in ASCII format.
- **File Filtering**: Excludes common binary files, cache directories, hidden files, and irrelevant artifacts to keep outputs concise and focused.
- Supports handling of non-UTF-8 and binary files gracefully.
- Customizable exclusions based on extensions and directory names.

## Customization

Modify the `SKIP_EXTENSIONS` and `SKIP_DIRS` variables in the script to exclude specific file types or directories according to your project's needs.

## Example

```bash
serialize-repo /Users/example_user/projects/my_repo repo_snapshot.txt
```

## Contributing

Pull requests and improvements are welcome! Please ensure your contributions are clearly documented and tested.