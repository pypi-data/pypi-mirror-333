# De-Ingest

A command-line tool to reverse a gitingest digest file and restore the original repository structure.

## Installation

Install via pip:

```bash
pip install deingest
```

Or install from source:

```bash
python setup.py install
```

## Usage

Restore files from a digest file: 

```bash
deingest -f /path/to/example/digest.txt -o /path/to/output/example/myproject -w
```

## Options

- **`-f, --file`**: Path to the digest file.  
- **`-o, --output`**: Output directory (defaults to the current directory).  
- **`-w, --overwrite`**: Overwrite existing files.  
- **`-d, --dry-run`**: Simulate restoration without writing files.  
- **`-v, --verbose`**: Enable verbose logging.  
- **`-h, --help`**: Display help message.  

