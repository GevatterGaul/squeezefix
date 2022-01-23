#!/usr/local/bin/python3
""" De-squeeze images shot on anamorphic lenses """


from argparse import ArgumentParser
from os import scandir
from posix import DirEntry
from pathlib import Path

from jpeg import handle_jpeg
from raf import handle_raf
from exiftool import get_metadata


def imorph(path: str, no_jpegs: bool = False, no_raws: bool = False, move_originals: bool = False):
    with scandir(path) as image_dir:
        for entry in image_dir:
            if isinstance(entry, DirEntry):
                filepath = Path(entry.path)
                image_metadata = get_metadata(filepath)

                if image_metadata['FileType'] == 'JPEG':
                    if not no_jpegs:
                        handle_jpeg(filepath, image_metadata, move_originals)
                    else:
                        print(f'Skipping "{filepath.as_posix()}": JPEG files will not be processed')
                elif image_metadata['FileType'] == 'RAF':
                    if not no_raws:
                        handle_raf(filepath, image_metadata, move_originals)
                    else:
                        print(f'Skipping "{filepath.as_posix()}": RAF files will not be processed')
                else:
                    print(f'Skipping "{filepath.as_posix()}": unknown file format')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('-j', '--no-jpeg', help='Don\'t consider jpeg images', action='store_true')
    parser.add_argument('-r', '--no-raw', help='Don\'t consider raw images', action='store_true')
    parser.add_argument('-m', '--move-originals', help='Move originals to subfolder', action='store_true')
    args = parser.parse_args()

    imorph(args.path, args.no_jpeg, args.no_raw, args.move_originals)
