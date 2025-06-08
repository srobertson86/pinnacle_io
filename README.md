# pinnacle_io

`pinnacle_io` is a local Python library for reading and writing Pinnacle radiotherapy treatment planning files using structured SQLAlchemy models. It enables conversion between Pinnacle’s internal file formats and Python-native data structures for inspection, validation, and transformation.

## Features

- Support for Institution, Patient, Plan and associated file types
- SQLAlchemy-backed models for easy data manipulation
- File readers and writers for Pinnacle text-based plan files
- Utility functions for extracting tar archives with disk space checks
- Optional GUI support for file content inspection
- Fully testable with `pytest`
- Ready for local development with `pip install -e .`

## Installation

```bash
git clone https://your.repo.url/pinnacle_io
cd pinnacle_io
pip install -e .
```

## Usage

```python
from pinnacle_io.readers.institution_reader import read_institution

institution = read_institution("/path/to/Institution")
print(institution.name)
```

