import pandas as pd
import numpy as np
import os

path = os.getcwd() + '/specs/'
path_save = os.getcwd() + '/txts/'


def convert_to_txt(file_ori, file_tar):
    df = pd.read_excel(file_ori,sheet_name=0)
    np.savetxt(file_tar, df.values, delimiter='#', encoding='utf-8', fmt="%s")


for file in os.listdir(path):
    if 'xlsx' in file:
        _p1 = os.path.join(path, file)
        _p2 = os.path.join(path_save, file.replace('xlsx', 'txt'))
        convert_to_txt(_p1,_p2)

