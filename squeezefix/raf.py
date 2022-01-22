from pathlib import Path
from shutil import move
from subprocess import run

from wand.image import Image

from squeezefix.helpers import ensure_originals_folder
from squeezefix.jpeg import generate_jpeg_thumbnail, set_and_delete_jpeg_thumbnail, resize_srgb
from squeezefix.metadata import is_anamorphic, calculate_new_size, ANAMORPHIC_SCALE_FACTOR


def handle_raf(filepath: Path, move_original: bool = False):
    converted_dng_path = convert_raf(filepath)

    with Image(filename=converted_dng_path.as_posix()) as img:
        if is_anamorphic(img):
            set_dng_anamorphic_ratio(converted_dng_path)
            add_thumbnails_to_dng(img, converted_dng_path)

            if move_original:
                target_folder = ensure_originals_folder(filepath)
                target_filepath = Path(target_folder, filepath.name)
                move(filepath, target_filepath)
                print(f'Processed "{filepath.as_posix()}", original at {target_filepath.as_posix()}')
            else:
                print(f'Processed "{filepath.as_posix()}"')
        else:
            converted_dng_path.unlink()


def add_thumbnails_to_dng(img: Image, filepath: Path):
    jpeg = generate_jpeg_from_raw(img)

    preview_path = Path(filepath.parent, filepath.stem + '_PreviewImage.jpg')
    generate_jpeg_thumbnail(jpeg, preview_path, 1024)
    set_and_delete_jpeg_thumbnail(filepath, preview_path, 'PreviewImage')

    jpeg_path = Path(filepath.parent, filepath.stem + '_JpgFromRaw.jpg')
    jpeg.save(filename=jpeg_path.as_posix())
    set_and_delete_jpeg_thumbnail(filepath, jpeg_path, 'JpgFromRaw')


def generate_jpeg_from_raw(img: Image):
    jpeg = img.clone()
    jpeg.format = 'jpeg'
    jpeg.compression_quality = 95
    width, height = calculate_new_size(img)
    resize_srgb(jpeg, width, height)
    return jpeg


def convert_raf(filepath: Path) -> Path:
    run([
        '/Applications/Adobe DNG Converter.app/Contents/MacOS/Adobe DNG Converter',
        '-p2',
        filepath.as_posix()
    ], capture_output=True).check_returncode()

    return Path(filepath.parent, filepath.stem + '.dng')


def set_dng_anamorphic_ratio(filepath: Path):
    run([
        'exiftool',
        '-overwrite_original_in_place',
        f'-DefaultScale={ANAMORPHIC_SCALE_FACTOR} 1',
        filepath.as_posix()
    ], capture_output=True).check_returncode()