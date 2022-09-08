import pandas as pd
from utils import ann_folder, json_folder, text_folder, get_filestar_name, read_txt, get_filename_no_ext


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


def new_ann():
    pass

def main():
    df = pd.read_excel("out - Copy.xlsx")
    for ind in df.index:
        r = ReviewedAnnotation(df['filename'][ind], df['testo'][ind], df['entità rilevata'][ind], df["valido"][ind])
        if r.valid:
            annotations_for_current_file = ann_folder.glob(f'**/{get_filestar_name(r.txt_filename)}')
            for file in annotations_for_current_file:
                content = read_txt(file)
                if r.domain in content:
                    print("pass")
                else:
                    ann_numbers = []
                    for f in ann_folder.glob(f'**/{get_filestar_name(file)}'):
                        ann_numbers.append(get_filename_no_ext(f)[-1])
            if ann_numbers:
                next_ann_for_file = get_filename_no_ext(r.txt_filename)[:-1] + str(int(max(ann_numbers))+1)
                with open(f"ann/new/{next_ann_for_file}.ann", "a", encoding="utf-8") as ann:
                    tax_count = 1
                    ann.write(f"C{tax_count}		{r.domain}\n")


if __name__ == "__main__":
    main()