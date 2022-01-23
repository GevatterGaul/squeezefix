""" File handling helper functions """
from pathlib import Path


def ensure_originals_folder(filepath: Path) -> Path:
    target_folder = Path(filepath.parent, 'originals')
    target_folder.mkdir(exist_ok=True)
    return target_folder
