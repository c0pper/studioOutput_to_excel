import pandas as pd
from utils import ann_folder, json_folder, text_folder

df = pd.read_excel("out - Copy.xlsx")

valid = df[df['valido'].str.contains('si')]
invalid = df[df['valido'].str.contains('no')]


# valid
for ind in valid.index:
    txt_filename = valid['filename'][ind]
    ann_filename = txt_filename.split(".")[0] + ".ann"
    text = valid['testo'][ind]
    domain = valid['entità rilevata'][ind]

