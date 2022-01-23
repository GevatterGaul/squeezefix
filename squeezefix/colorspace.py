""" Helper functions around color space """

import piexif
from wand.image import Image


def has_adobergb_colorspace(img: Image) -> bool:
    """ Has an image AdobeRGB colorspace

    The exif tag will show "uncalibrated" and the InteropIndex has the value "R03"

    https://exiftool.org/TagNames/EXIF.html
    """
    if 'exif:ColorSpace' in img.metadata and img.metadata['exif:ColorSpace'] == '65535':
        exif_bytes = img.profiles['exif']
        exif = piexif.load(exif_bytes)

        if 'Interop' in exif:
            return exif['Interop'][1] == b'R03'

    return False


def has_srgb_colorspace(img: Image) -> bool:
    """ Has an image sRGB colorspace

    This is easy: the value has to be 1

    https://exiftool.org/TagNames/EXIF.html
    """
    return 'exif:ColorSpace' in img.metadata and \
           img.metadata['exif:ColorSpace'] == '1'
