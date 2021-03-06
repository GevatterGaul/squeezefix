# Motivation

Script to resize and sort Fuji JPEG and RAW files that have been captured with anamorphic lenses.

The intended use case is to run the script over a directory of original files. Then import the resulting files into your raw converter of choice.

# Implementation Details

For some details on the implementation and its tradeoffs, go to the [announcement post](https://boredconsultant.com/2021/01/17/De-squeeze-anamorphic-images-with-squeezefix/).

# Compatibility

Developed for Fuji Cameras and SIRUI anamorphic lenses.

Tested on Fuji X-T10 and SIRUI 50mm 1.8 anamorphic (squeeze factor 1.33).

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