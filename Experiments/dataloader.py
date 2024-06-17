import os
import pandas as pd
from PIL import Image
import numpy as np

def get_file_names(folder_path, num_files):
    files = os.listdir(folder_path)
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
    files = sorted(files)
    return files[:num_files]


def get_GT(path):
    columns = ['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4', 'script', 'text']
    df = pd.read_csv(path, delimiter=',', names=columns)
    # get df in format for evaluation
    gt = []
    for _, item in df.iterrows():
        gt.append(([[item.x1, item.y1], [item.x2, item.y2], [item.x3, item.y3], [item.x4, item.y4]], item.text))
    return gt
    

def get_GTs(dir, file_names):
    GTs = []
    for file_name in file_names:
        print(f"extracting {dir}/{file_name}")
        # get round truth as dataframe
        path = dir + "/" + file_name
        GTs.append(get_GT(path))
    return GTs


def get_image(path):
    image = np.asarray(Image.open(path).convert('RGB'))
    return image


def get_images(dir, file_names):
    images = []
    print()
    for file_name in file_names:
        print(f"extracting {dir}/{file_name}")
        path = dir +'/'+ file_name
        images.append(get_image(path))
    return images