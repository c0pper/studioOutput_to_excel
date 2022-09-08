from pathlib import Path
from typing import Union
import gzip
import json

ann_folder = Path("ann")
json_folder = Path("json")
text_folder = Path("text")


def get_filename_no_ext(path: Union[Path, str]):
    if isinstance(path, str):
        path = Path(path)
    path = path.stem.__str__()
    path = path.split(".")[0]
    return path





