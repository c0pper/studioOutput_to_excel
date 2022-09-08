from pathlib import Path
import gzip
import json
import pandas as pd
from typing import Union


def get_filename_no_ext(path: Union[Path, str]):
    if isinstance(path, str):
        path = Path(path)
    path = path.stem.__str__()
    path = path.split(".")[0]
    return path


def read_txt(filename: Union[Path, str]):
    if isinstance(filename, Path):
        filename = filename.__str__()
    with open(filename, encoding="UTF8") as txt:
        return txt.read()


def load_jsongz(filename: Union[Path, str]):
    with gzip.open(filename, "r") as f:
        data = f.read()
        j = json.loads(data.decode('utf-8'))
    return j


def get_begin_end_rulelabel(json_file: json) -> list:
    list_of_cats = []
    for x in json_file["match_info"]["rules"]["categorization"]:
        domain = x["name"]

        for r in x["rules"]:
            if r["label"]:
                rule_label = r["label"]
            else:
                rule_label = ""
            begin = r["scope"][0]["begin"]
            end = r["scope"][0]["end"] + 1
            single_cat_dict = {"domain": domain, "begin": begin, "end": end, "rule_label": rule_label}
            list_of_cats.append(single_cat_dict)
    return list_of_cats


def main():
    json_folder = Path("json")
    text_folder = Path("text")
    ctx_files = list(json_folder.glob('**/*.txt.ctx.json.gz'))

    all_categorizations = []
    for f in ctx_files:
        txt_name = get_filename_no_ext(f) + ".txt"
        loaded_json = load_jsongz(f)
        loaded_txt = read_txt(text_folder / txt_name)

        categorizations = get_begin_end_rulelabel(loaded_json)
        if categorizations:
            for c in categorizations:
                text_portion = loaded_txt[c["begin"]:c["end"]]
                dataframe_dict = {"testo": text_portion, "entità": c["domain"], "valido": ""}
                all_categorizations.append(dataframe_dict)
        df = pd.DataFrame(all_categorizations)
        df_unique = pd.DataFrame(df).drop_duplicates()
        df_unique.to_excel("out.xlsx", index=False)


if __name__ == "__main__":
    main()


