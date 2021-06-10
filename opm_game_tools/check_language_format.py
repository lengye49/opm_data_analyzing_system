import pandas as pd
import os


def compare_version(v1, v2):
    if len(v1.split(".")) < 3:
        return v2
    if len(v2.split(".")) < 3:
        return v1

    a, b, c = v1.split('.')
    A, B, C = v2.split('.')
    x = int(a) * 10000 + int(b) * 100 + int(c)
    y = int(A) * 10000 + int(B) * 100 + int(C)
    if x >= y:
        return v1
    else:
        return v2


def set_version_path():
    # _p = "/Users/oas/Documents/work/github/opm_specs/specs/"
    _p = os.path.abspath('../..') + "/specs/"
    folders = os.listdir(_p)
    current_version = folders[0]
    for folder in folders:
        current_version = compare_version(current_version, folder)

    global path
    path = _p + current_version + '/xlsx_design/languages.xlsx'


# <color, size, b, material
# <quad
# s = '<color=#111>hello <b> world </b> </color>'
# color_head = s.count('<color')
# color_end = s.count('/color')

def check_is_error(id, lang):
    if lang.count('<color') != lang.count('/color>'):
        print(id, ',color 代码不匹配,', lang)
    if lang.count('<size') != lang.count('/size>'):
        print(id, ',size 代码不匹配,', lang)
    if lang.count('<b') != lang.count('/b>'):
        print(id, ',b 代码不匹配,', lang)
    if lang.count('<material') != lang.count('/material>'):
        print(id, ',material 代码不匹配,', lang)
    if lang.count('<quad') != lang.count('/>'):
        print(id, ',size 代码不匹配,', lang)


path = ''
set_version_path()

language = pd.read_excel(path, sheet_name='英语', header=None)
print('正在检测处理英语：')
language.apply(lambda x: check_is_error(x[0], str(x[1])), axis=1)
print('处理完毕')

language = pd.read_excel(path, sheet_name='德语', header=None)
print('正在检测处理德语：')
language.apply(lambda x: check_is_error(x[0], str(x[1])), axis=1)
print('处理完毕')

language = pd.read_excel(path, sheet_name='法语', header=None)
print('正在检测处理法语：')
language.apply(lambda x: check_is_error(x[0], str(x[1])), axis=1)
print('处理完毕')

language = pd.read_excel(path, sheet_name='西语', header=None)
print('正在检测处理西语：')
language.apply(lambda x: check_is_error(x[0], str(x[1])), axis=1)
print('处理完毕')

language = pd.read_excel(path, sheet_name='葡语', header=None)
print('正在检测处理葡语：')
language.apply(lambda x: check_is_error(x[0], str(x[1])), axis=1)
print('处理完毕')

language = pd.read_excel(path, sheet_name='土语', header=None)
print('正在检测处理土语：')
language.apply(lambda x: check_is_error(x[0], str(x[1])), axis=1)
print('处理完毕')

language = pd.read_excel(path, sheet_name='俄语', header=None)
print('正在检测处理俄语：')
language.apply(lambda x: check_is_error(x[0], str(x[1])), axis=1)
print('处理完毕')
