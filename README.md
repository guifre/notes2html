# notes2html [![Build Status](https://travis-ci.org/guifre/notes2html.svg?branch=master)](https://travis-ci.org/guifre/notes2html.svg?branch=master) [![Coverage Status](https://coveralls.io/repos/github/guifre/notes2html/badge.svg?branch=master)](https://coveralls.io/github/guifre/notes2html?branch=master)

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

### Syntax

```text
*Document title*
Title one
    paragraph one *bold*
    *start of code
    end of code*
    #image#
```
