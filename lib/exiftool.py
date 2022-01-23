""" Wrapper functions around exiftool """
from typing import Dict
from subprocess import run
from pathlib import Path
import json


def get_metadata(filepath: Path) -> Dict:
    result = run([
        'exiftool',
        '-j',
        filepath.as_posix()
    ], check=True, capture_output=True)

    return json.loads(result.stdout)[0]
