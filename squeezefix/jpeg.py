""" jpeg image helper functions """

from pathlib import Path
from shutil import move
from subprocess import run
from typing import Optional, Dict

from wand.image import Image
from wand.color import Color

from colorspace import has_adobergb_colorspace, has_srgb_colorspace
from helpers import ensure_originals_folder
from metadata import is_anamorphic, adjust_exif, calculate_desqueezed_size, get_scaled_size


JPEG_COMPRESSION_QUALITY = 95
LINEAR_RGB_GAMMA = 0.4547069271758437
ADOBE_RGB_GAMMA = 2.19921875
BLACK = Color('black')


def resize_srgb(img: Image, new_width: int, new_height: int):
    """ Resize sRGB image with colospace conversion

    Just resizing would destroy image data. See: https://legacy.imagemagick.org/Usage/resize/#resize_colorspace
    """
    img.depth = 16
    img.transform_colorspace('rgb')
    img.resize(new_width, new_height, filter='lanczos2')
    img.transform_colorspace('srgb')
    img.depth = 8


def resize_adobergb(img: Image, new_width: int, new_height: int):
    """ Resize AdobeRGB image with colorspace correction

    Just resizing would destroy image data. See: https://legacy.imagemagick.org/Usage/resize/#resize_colorspace
    """
    img.depth = 16
    img.gamma(LINEAR_RGB_GAMMA)
    img.resize(new_width, new_height, filter='lanczos2')
    img.gamma(ADOBE_RGB_GAMMA)
    img.depth = 8


def rescale_srbg_or_adobergb_jpeg(img: Image, image_metadata: Dict, filepath: Path) -> Optional[Path]:
    new_width, new_height = calculate_desqueezed_size(img)
    new_path = Path(filepath.parent, filepath.stem + '_resized.jpg')

    if has_srgb_colorspace(image_metadata):
        resize_op = resize_srgb
    else:
        resize_op = resize_adobergb

    adjust_exif(img, new_width, new_height)
    resize_op(img, new_width, new_height)

    img.compression_quality = JPEG_COMPRESSION_QUALITY
    img.save(filename=new_path.as_posix())

    return new_path


def generate_and_set_jpeg_thumbnails(img: Image, filepath: Path) -> None:
    thumbnail_path = Path(filepath.parent, filepath.stem + '_thumbnail.jpg')
    generate_jpeg_thumbnail(img, thumbnail_path, 160, 120)
    set_and_delete_jpeg_thumbnail(filepath, thumbnail_path, 'ThumbnailImage')


def set_and_delete_jpeg_thumbnail(filepath: Path, thumbnail_path: Path, thumbnail_id: str):
    run([
        'exiftool',
        '-overwrite_original_in_place',
        f'-{thumbnail_id}<={thumbnail_path.as_posix()}',
        filepath.as_posix()
    ], capture_output=True, check=True)
    thumbnail_path.unlink()


def generate_jpeg_thumbnail(img: Image, path: Path, width: int, height: int = None):
    thumbnail = img.clone()
    thumbnail.format = 'jpeg'
    thumbnail.compression_quality = 95

    thumbnail_width, thumbnail_height = get_scaled_size(thumbnail, width)
    thumbnail.thumbnail(thumbnail_width, thumbnail_height)

    if height is not None and height > thumbnail_height:
        thumbnail_height_offset = round((height - thumbnail_height) / 2) * -1
        thumbnail.background_color = BLACK
        thumbnail.extent(width, height, 0, thumbnail_height_offset)

    thumbnail.save(filename=path.as_posix())


def handle_jpeg(filepath: Path, image_metadata: Dict, move_original: bool = False):
    if is_anamorphic(image_metadata):
        if (has_srgb_colorspace(image_metadata) or has_adobergb_colorspace(image_metadata)):
            with Image(filename=filepath.as_posix()) as img:
                new_path = rescale_srbg_or_adobergb_jpeg(img, image_metadata, filepath)
                generate_and_set_jpeg_thumbnails(img, new_path)

                if move_original:
                    target_folder = ensure_originals_folder(filepath)
                    target_filepath = Path(target_folder, filepath.name)
                    move(filepath, target_filepath)
                    move(new_path, filepath)
                    print(f'Processed "{filepath.as_posix()}", original at {target_filepath.as_posix()}')
                else:
                    print(f'Processed "{filepath.as_posix()}"')
        else:
            print(f'Skipping "{filepath.as_posix()}": unknown color space')
