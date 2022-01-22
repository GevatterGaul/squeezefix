#!/usr/local/bin/python3
from argparse import ArgumentParser
from os import scandir
from posix import DirEntry
from pathlib import Path

from squeezefix.helpers import is_raf, is_jpeg
from squeezefix.jpeg import handle_jpeg
from squeezefix.raf import handle_raf


def imorph(path: str, no_jpegs: bool = False, no_raws: bool = False, move_originals: bool = False):
    with scandir(path) as dir:
        for entry in dir:
            if isinstance(entry, DirEntry):
                filepath = Path(entry.path)

                if is_jpeg(entry):
                    if not no_jpegs:
                        handle_jpeg(filepath, move_originals)
                    else:
                        print(f'Skipping "{filepath.as_posix()}": JPEG files will not be processed')
                elif is_raf(entry):
                    if not no_raws:
                        handle_raf(filepath, move_originals)
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