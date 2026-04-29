# notes2html [![CI](https://github.com/guifre/notes2html/actions/workflows/ci.yml/badge.svg)](https://github.com/guifre/notes2html/actions/workflows/ci.yml) [![Coverage Status](https://coveralls.io/repos/github/guifre/notes2html/badge.svg?branch=master)](https://coveralls.io/github/guifre/notes2html?branch=master)

I write notes of random topics and I wanted to keep them online for easy access. However, I hate writing HTML.

notes2html transforms my notes to basic HTML. The workflow is just writing and pushing a note. After this, a git hook triggers a notes2html job that builds the notes and synchronizes it to http://guif.re

## Usage

Run with Python 3 and pass the source notes directory plus the destination HTML directory:

```bash
python3 notes2html.py path/to/notes path/to/html
```

The converter recursively finds `.txt` files under the source directory and writes matching `.html` files under the destination directory.

## Tests

Run the unit tests with:

```bash
python3 -m unittest discover
```

To generate coverage locally:

```bash
python3 -m coverage run -m unittest discover
python3 -m coverage html
```

Optional development tools are configured in `pyproject.toml`. After installing the dev dependencies, run:

```bash
python3 -m tox
python3 -m ruff check .
python3 -m ruff format .
```

## CI

GitHub Actions runs the unit test suite on Python 3.10, 3.11, 3.12, and 3.13. The CI workflow runs tests with `coverage` and uploads the Python 3.13 coverage report to Coveralls.

### Syntax

```text
*Document title*
Title one
    paragraph one *bold*
    *start of code
    end of code*
    #image#
```
