"""
Helper functions dealing with image metadata
"""
import re
from typing import Tuple, Dict

import piexif
from wand.image import Image


POSSIBLE_ANAMORPHIC_FOCAL_LENGTHS = [24, 50]
ANAMORPHIC_SCALE_FACTOR = 1.33


def is_anamorphic(image_metadata: Dict) -> bool:
    match = re.match(r'(\d+)\.\d+ mm', image_metadata['FocalLength'])
    focal_length = int(match.group(1))

    return focal_length in POSSIBLE_ANAMORPHIC_FOCAL_LENGTHS and image_metadata['FNumber'] == 'undef'


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
