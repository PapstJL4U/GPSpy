import pandas as pd
from matplotlib import image as mimage
from matplotlib import pyplot as plt
import my_data as md
import smopy as sm
import os
from pathlib import Path

def load_all_tiles()->list:
    """Build a dictionary of tiles with relevenat data"""
    tile_dic = {}
    print('Using the following files:')
    for file in os.listdir(md.tiles_folder):
        if file.lower().endswith('.png'):
            _, tile_id, zoom, lon, lat = file.removesuffix(".png").split('_')
            tile_dic.update({tile_id : (zoom, lon, lat, file)})
    return tile_dic

def buil_image_from_tiles(tile_dic:dict)->None:
    """build a full sized image from thiles"""
    for tile_id, (zoom, lon, lat, file) in tile_dic.items():
        mimage.imread(os.path.join(md.tiles_folder, file))


if __name__ == "__main__":
    load_all_tiles()
