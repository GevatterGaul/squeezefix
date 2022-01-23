"""
Helper functions dealing with image metadata
"""

from typing import Union, Tuple

import piexif
from wand.image import Image


POSSIBLE_ANAMORPHIC_FOCAL_LENGTHS = [24, 50]
ANAMORPHIC_SCALE_FACTOR = 1.33


def convert_dng_focallength(wand_focallength: str) -> int:
    flength, _ = wand_focallength.split(',')
    return int(flength)


def convert_jpeg_focallength(wand_focallength: str) -> int:
    numerator, denominator = wand_focallength.split('/')
    return round(float(numerator) / float(denominator))


def convert_dng_fnumber(wand_fnumber: str) -> Union[float, None]:
    """ Convert """
    if wand_fnumber in ['F/nan', 'F/1,0']:
        return None

    _, fnum = wand_fnumber.split('/')
    return float(fnum.replace(',', '.'))


def convert_jpeg_fnumber(wand_fnumber: str) -> Union[float, None]:
    if wand_fnumber == '0/0':
        return None

    numerator, denominator = wand_fnumber.split('/')
    return float(numerator) / float(denominator)


def is_anamorphic(img: Image) -> bool:
    if img.format == 'DNG':
        focal_length_match = 'dng:FocalLength' in img.metadata and \
            convert_dng_focallength(img.metadata['dng:FocalLength']) in POSSIBLE_ANAMORPHIC_FOCAL_LENGTHS
        fnumber_match = 'dng:Aperture' in img.metadata and convert_dng_fnumber(img.metadata['dng:Aperture']) is None
    else:
        focal_length_match = 'exif:FocalLength' in img.metadata and \
            convert_jpeg_focallength(img.metadata['exif:FocalLength']) in POSSIBLE_ANAMORPHIC_FOCAL_LENGTHS
        fnumber_match = 'exif:FNumber' in img.metadata and convert_jpeg_fnumber(img.metadata['exif:FNumber']) is None

    return focal_length_match and fnumber_match


def adjust_exif(img: Image, width: int, height: int):
    exif_bytes = img.profiles['exif']
    exif = piexif.load(exif_bytes)

    exif['Exif'][piexif.ExifIFD.PixelXDimension] = width
    exif['Exif'][piexif.ExifIFD.PixelYDimension] = height

    new_exif_bytes = piexif.dump(exif)
    img.profiles['exif'] = new_exif_bytes


def calculate_desqueezed_size(img: Image) -> Tuple[int, int]:
    is_portrait = img.width < img.height

    if is_portrait:
        new_width = img.width
        new_height = round(img.height * ANAMORPHIC_SCALE_FACTOR)
    else:
        new_width = round(img.width * ANAMORPHIC_SCALE_FACTOR)
        new_height = img.height

    return new_width, new_height


def get_scaled_size(img: Image, new_width: int) -> (int, int):
    return new_width, round(new_width*img.height/img.width)
