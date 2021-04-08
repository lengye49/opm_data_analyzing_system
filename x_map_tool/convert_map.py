import pandas as pd
import os
import xml.etree.ElementTree as Et

cur_path = '/Users/oas/Documents/work/github/xiakexing/Maps/'
img_w = None
img_g = None
img_i = None

# find csvs from map directory
def get_csvs(_path):
    ground = []
    item = []
    walkable = []
    for file in os.listdir(_path):
        if '_csv' in file:
            s = file.strip('_csv')
            _ground_path = os.path.join(_path,file,s + '_ground.csv')
            if not os.path.exists(_ground_path):
                print('can not find ' + _ground_path)
                continue
            _item_path = os.path.join(_path, file, s + '_item.csv')
            if not os.path.exists(_item_path):
                print('can not find ' + _item_path)
                continue
            _walkable_path = os.path.join(_path, file, s + '_walkable.csv')
            if not os.path.exists(_walkable_path):
                print('can not find ' + _walkable_path)
                continue
            ground.append(_ground_path)
            item.append(_item_path)
            walkable.append(_walkable_path)
    return ground, item, walkable


# get image_names
def get_images(_path):
    if not os.path.exists(_path):
        print('can not find tsx: ' + _path)

    data = {}
    tree = Et.parse(_path)
    root = tree.getroot()
    for tile in root.findall("tile"):
        id = int(tile.get("id"))
        image = tile.find("image")
        if image is None:
            continue

        source = image.get("source")
        if source.rfind("/") != -1:
            source = source[source.rfind("/") + 1:]
        if source.find(".") != -1:
            source = source[:source.find(".")]
        data[id] = source
    return data


def convert(_g, _i, _w):
    _map = ''
    df_g = pd.read_csv(_g)
    df_g = df_g.applymap(lambda v: img_g[v] if v > 0 else v)
    df_i = pd.read_csv(_i)
    df_i = df_i.applymap(lambda v: img_i[v] if v > 0 else v)
    df_w = pd.read_csv(_w)
    print(1)


def get_data(scene):
    _path = os.path.join(cur_path, scene)
    _map_path = os.path.join(_path, 'maps')
    if os.path.exists(_map_path):
        global img_g
        img_g = get_images(os.path.join(_path, 'ground.tsx'))
        global img_i
        img_i = get_images(os.path.join(_path, 'item.tsx'))

        ground_list, item_list, walkable_list = get_csvs(_map_path)
        for i in range(0, len(ground_list)):
            convert(ground_list[i], item_list[i], walkable_list[i])



def main():
    global img_w
    img_w = get_images(os.path.join(cur_path, 'common.tsx'))

    for file in os.listdir(cur_path):
        if 'scene' in file:
            get_data(file)


if __name__ == '__main__':
    main()