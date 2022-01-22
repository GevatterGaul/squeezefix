from posix import DirEntry
from pathlib import Path


def is_jpeg(file: DirEntry) -> bool:
    name = file.name.lower()
    return name.endswith('.jpg') or name.endswith('.jpeg')


def is_raf(file: DirEntry) -> bool:
    name = file.name.lower()
    return name.endswith('.raf')


def ensure_originals_folder(filepath: Path) -> Path:
    target_folder = Path(filepath.parent, 'originals')
    target_folder.mkdir(exist_ok=True)
    return target_folder
