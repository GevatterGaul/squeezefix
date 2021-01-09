#!/usr/local/bin/python3
from argparse import ArgumentParser
from os import scandir
from posix import DirEntry
from pathlib import Path
from typing import Tuple, Union

import piexif
from wand.image import Image


POSSIBLE_ANAMORPHIC_FOCAL_LENGTHS = [24, 50]
ANAMORPHIC_SCALE_FACTOR = 1.33
LINEAR_RGB_GAMMA = 0.4547069271758437
ADOBE_RGB_GAMMA = 2.19921875
JPEG_COMPRESSION_QUALITY = 95


def is_jpeg(file: DirEntry) -> bool:
    name = file.name.lower()
    return name.endswith('.jpg') or name.endswith('.jpeg')


def is_raf(file: DirEntry) -> bool:
    name = file.name.lower()
    return name.endswith('.raf')


def convert_exif_number(enum: str) -> Union[float, None]:
    if enum == '0/0':
        return None
    numerator, denominator = enum.split('/')
    return float(numerator)/float(denominator)


def is_anamorphic(img: Image) -> bool:
    focal_length_match = 'exif:FocalLength' in img.metadata and \
                         int(convert_exif_number(img.metadata['exif:FocalLength'])) in POSSIBLE_ANAMORPHIC_FOCAL_LENGTHS
    fnumber_match = 'exif:FNumber' in img.metadata and convert_exif_number(img.metadata['exif:FNumber']) is None

    return focal_length_match and fnumber_match


def has_adobergb_colorspace(img: Image) -> bool:
    if 'exif:ColorSpace' in img.metadata and img.metadata['exif:ColorSpace'] == '65535':
        exif_bytes = img.profiles['exif']
        exif = piexif.load(exif_bytes)

        if 'Interop' in exif:
            return exif['Interop'][1] == b'R03'

    return False


def has_srgb_colorspace(img: Image) -> bool:
    return 'exif:ColorSpace' in img.metadata and \
           img.metadata['exif:ColorSpace'] == '1'


def adjust_exif(img: Image, width: int, height: int):
    exif_bytes = img.profiles['exif']
    exif = piexif.load(exif_bytes)

    exif['Exif'][piexif.ExifIFD.PixelXDimension] = width
    exif['Exif'][piexif.ExifIFD.PixelYDimension] = height

    new_exif_bytes = piexif.dump(exif)
    img.profiles['exif'] = new_exif_bytes


def rescale_jpeg(img: Image, filepath: Path) -> None:
    new_height, new_width = calculate_new_size(img)
    new_path = Path(filepath.parent, filepath.stem + '_resized.jpg')

    if has_adobergb_colorspace(img):
        resize_op = resize_adobergb
    elif has_srgb_colorspace(img):
        resize_op = resize_srgb
    else:
        print(f'Skipping "{filepath.as_posix()}": unknown color space')
        return

    adjust_exif(img, new_width, new_height)
    resize_op(img, new_width, new_height)

    img.compression_quality = JPEG_COMPRESSION_QUALITY
    img.save(filename=new_path.as_posix())


def calculate_new_size(img: Image) -> Tuple[int, int]:
    is_portrait = img.width < img.height

    if is_portrait:
        new_width = img.width
        new_height = round(img.height * ANAMORPHIC_SCALE_FACTOR)
    else:
        new_width = round(img.width * ANAMORPHIC_SCALE_FACTOR)
        new_height = img.height

    return new_height, new_width


def resize_srgb(img: Image, new_width: int, new_height: int):
    img.depth = 16
    img.transform_colorspace('rgb')
    img.resize(new_width, new_height, filter='lanczos2')
    img.transform_colorspace('srgb')
    img.depth = 8


def resize_adobergb(img: Image, new_width: int, new_height: int):
    img.depth = 16
    img.gamma(LINEAR_RGB_GAMMA)
    img.resize(new_width, new_height, filter='lanczos2')
    img.gamma(ADOBE_RGB_GAMMA)
    img.depth = 8


def imorph(path: str):
    with scandir(path) as dir:
        for entry in dir:
            if isinstance(entry, DirEntry) and is_jpeg(entry):
                with Image(filename=entry.path) as img:
                    if is_anamorphic(img):
                        rescale_jpeg(img, Path(entry.path))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()

    imorph(args.path)