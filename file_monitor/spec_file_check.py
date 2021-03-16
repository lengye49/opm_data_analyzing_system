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


def get_version_path():
    _p = os.path.abspath('..') + "/specs/"
    folders = os.listdir(_p)
    current_version = folders[0]
    for folder in folders:
        current_version = compare_version(current_version, folder)

    return _p + current_version + '/'


csv_path = os.path.abspath('..') + '/csvs'
excel_path = get_version_path()

csv_list = os.listdir(csv_path)
csv_list.remove('common')
csv_list.remove('server_json.txt')
if '.gitignore' in csv_list:
    csv_list.remove('.gitignore')
if '.DS_Storein' in csv_list:
    csv_list.remove('.DS_Storein')

excel_list = os.listdir(excel_path)
excel_list.remove('languages')
excel_list.remove('languages_client')
excel_list.remove('xlsx_design')
excel_list.remove('xlsx_origin')

for x in csv_list:
    if x not in excel_list:
        print('\n\n\n\nCan not find csv directory server:' + str(x) + ' in excel_origin!\n\n\n\n')
