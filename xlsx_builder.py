import pandas as pd
import json
from utils import get_filename_no_ext, json_folder, ann_folder, text_folder
from typing import Union
from pathlib import Path
import gzip


class Categorization():
    def __init__(self, json_filename: Union[Path, str]):
        self.json_filename = json_filename
        self.basename = get_filename_no_ext(json_filename)
        self.ann_name = self.basename + ".ann"
        self.txt_name = self.basename + ".txt"
        self.loaded_json = self.load_jsongz()
        self.loaded_ann = self.read_txt(ann_folder / self.ann_name)
        self.loaded_txt = self.read_txt(text_folder / self.txt_name)

    def load_jsongz(self):
        with gzip.open(self.json_filename, "r") as f:
            data = f.read()
            j = json.loads(data.decode('utf-8'))
        return j

    def read_txt(self, path: Union[Path, str]):
        if isinstance(path, Path):
            path = path.__str__()
        with open(path, encoding="UTF8") as txt:
            return txt.read()

    def get_list_of_categorizations(self) -> list:
        list_of_cats = []
        for x in self.loaded_json["match_info"]["rules"]["categorization"]:
            domain = x["name"]

            file_starname = self.basename[:-1] + "*"
            for file in ann_folder.glob(f'**/{file_starname}'):
                print(file)
                content = self.read_txt(file)
                if domain in content:
                    pass
                else:
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
    ctx_files = list(json_folder.glob('**/*.txt.ctx.json.gz'))

    all_categorizations = []
    for f in ctx_files:
        cat_obj = Categorization(f)
        categorizations = cat_obj.get_list_of_categorizations()

        if categorizations:
            for c in categorizations:
                text_portion = cat_obj.loaded_txt[c["begin"]:c["end"]]
                dataframe_dict = {"filename": cat_obj.txt_name, "testo": text_portion, "entità rilevata": c["domain"],
                                  "valido": ""}
                all_categorizations.append(dataframe_dict)

        df = pd.DataFrame(all_categorizations)
        df_unique = pd.DataFrame(df).drop_duplicates()
        df_unique.to_excel("out.xlsx", index=False)


if __name__ == "__main__":
    main()
