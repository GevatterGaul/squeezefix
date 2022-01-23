# Motivation

Script to resize and sort Fuji JPEG and RAW files that have been captured with anamorphic lenses.

The intended use case is to run the script over a directory of original files. Then import the resulting files into your raw converter of choice.

# Implementation Details

For some details on the implementation and its tradeoffs, go to the [announcement post](https://boredconsultant.com/2021/01/17/De-squeeze-anamorphic-images-with-squeezefix/).

## Metadata formats

There are a bunch of different metadata formats and their representation in various libraries is confusing. Here are some places to start:

- https://exiftool.org/TagNames/EXIF.html
- https://www.adobe.com/content/dam/acom/en/products/photoshop/pdfs/dng_spec_1.4.0.0.pdf

# Compatibility

Developed for Fuji Cameras and SIRUI anamorphic lenses.

## Cameras

- Fujifilm X-T10
- Fujifilm X-T4

# Lenses

- SIRUI 50mm anamorphic
- SIRUI 24mm anamorphic

# Requirements

The requirements for MacOS:

```bash
brew install exiftool imagemagick ufraw python pipenv
```

You also need the Adobe Digital Negative Converter.

# Setup

Clone the repository to a directory. There, execute:

```bash
pipenv install
```

# Usage

Convert all files in the ```raw``` directory and save the original files in ```raw/originals```:

```bash
python squeezefix.py -m raw/
```

Other options:

```
# python anamorfix.py -h
usage: squeezefix.py [-h] [-j] [-r] [-m] path

positional arguments:
  path

optional arguments:
  -h, --help            show this help message and exit
  -j, --only-jpeg       Only consider jpeg images
  -r, --only-raw        Only consider raw images
  -m, --move-originals  Move originals to subfolder

```