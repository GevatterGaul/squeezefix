""" Helper functions around color space """
from typing import Dict


def has_adobergb_colorspace(image_metadata: Dict) -> bool:
    """ Has an image AdobeRGB colorspace

    The exif tag will show "uncalibrated" and the InteropIndex has the value "R03"

    https://exiftool.org/TagNames/EXIF.html
    """
    return image_metadata['ColorSpace'] == 'Uncalibrated' and image_metadata['InteropIndex'].startswith('R03')


def has_srgb_colorspace(image_metadata: Dict) -> bool:
    """ Has an image sRGB colorspace

    This is easy: the value has to be 1

    https://exiftool.org/TagNames/EXIF.html
    """
    return image_metadata['ColorSpace'] == 'sRGB'
