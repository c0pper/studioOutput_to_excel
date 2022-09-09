import pandas as pd
from utils import ann_folder, json_folder, text_folder, get_filestar_name, read_txt, get_filename_no_ext
from pathlib import Path


class ReviewedAnnotation:
    def __init__(self, txt_filename: str, text: str, domain: str, valid: str):
        self.txt_filename = txt_filename
        self.ann_filename = self.txt_filename.split(".")[0] + ".ann"
        self.text = text
        self.domain = domain
        if "si" in valid:
            self.valid = True
        else:
            self.valid = False


def main():
    df = pd.read_excel("out - Copy.xlsx")
    for ind in df.index:
        print("-"*10)
        r = ReviewedAnnotation(df['filename'][ind], df['testo'][ind], df['entità rilevata'][ind], df["valido"][ind])
        if r.valid:
            annotations_for_current_file = list(ann_folder.glob(f'**/{get_filestar_name(r.txt_filename)}'))
            ann_numbers = [] # numeri dei sottofile con singole annotazioni
            domains_for_current_file = []
            for f in annotations_for_current_file:
                print(f"\ncurrent: {f}")
                ann_numbers.append(get_filename_no_ext(f)[-1])
                content = read_txt(f)
                content = content.split("\t")[-1].strip()
                domains_for_current_file.append(content)
                print(f"tabella excel - {r.domain} vs annotazione - {content}")
                if r.domain in set(domains_for_current_file):
                    print(f"breaking on {r.txt_filename}, {r.domain} already in {set(domains_for_current_file)}")
                    break
                next_ann_num = int(max(ann_numbers)) + 1
                next_ann_name = get_filename_no_ext(r.txt_filename)[:-1] + str(next_ann_num)

                if not Path(f"ann/{next_ann_name}.ann").is_file():
                    print(f"ann {next_ann_name} not exist, creating")
                    with open(f"ann/{next_ann_name}.ann", "a", encoding="utf-8") as ann:
                        print(f"C1		{r.domain}\n")
                        ann.write(f"C1		{r.domain}\n")
                    with open(f"text/{next_ann_name}.txt", "a", encoding="utf-8") as txt:
                        print(r.text)
                        txt.write(r.text)
                else:
                    print(f"ann {next_ann_name} already exists")


if __name__ == "__main__":
    main()