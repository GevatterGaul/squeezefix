# Motivation

Script to resize and sort JPEG and RAW Fuji Files that have been captured with anamorphic lenses.

The intended use case is to run the script over a directory of original files. Then import the resulting files into your raw converter of choice.

# Requirements

The requirements for MacOS:

```bash
brew install exiftool imagemagick ufraw python pipenv
```

# Setup

Clone the repository to a directory. There, execute:

```bash
pipenv install
```

# Usage

Convert all files in the ```raw``` directory and save the original files in ```raw/originals```:

```bash
python anamorfix.py -m raw/
```

Other options:

```
# python anamorfix.py -h
usage: anamorfix.py [-h] [-j] [-r] [-m] path

positional arguments:
  path

optional arguments:
  -h, --help            show this help message and exit
  -j, --only-jpeg       Only consider jpeg images
  -r, --only-raw        Only consider raw images
  -m, --move-originals  Move originals to subfolder

```