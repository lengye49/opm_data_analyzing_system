import os
import glob
import pandas as pd
from distutils.version import StrictVersion


def load_specs(table):
    path = '../specs/'
    list_versions = [os.path.basename(f) for f in glob.glob(f'{path}*.*.*')]
    list_versions = sorted(list_versions, key=StrictVersion)
    latest_version = list_versions[-1]

    pathname = f'{path}{latest_version}/xlsx_origin/{table}.xlsx'
    df = pd.read_excel(pathname, header=3, sheet_name=table)
    df = df.drop(index=0)
    df = df.dropna(how='all')
    return df
