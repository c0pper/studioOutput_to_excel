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


def get_filestar_name(filename: str):
    return get_filename_no_ext(filename)[:-1] + "*"

def load_jsongz(json_filename: Union[Path, str]) -> json:
    if isinstance(json_filename, Path):
        json_filename = json_filename.__str__()
    with gzip.open(json_filename, "r") as f:
        data = f.read()
        j = json.loads(data.decode('utf-8'))
    return j

def read_txt(path: Union[Path, str]):
    if isinstance(path, Path):
        path = path.__str__()
    with open(path, encoding="UTF8") as txt:
        return txt.read()