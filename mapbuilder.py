from tkinter import E
import pandas as pd
from matplotlib import image as mimage
from matplotlib import pyplot as plt
import my_data as md
import smopy as sm
import networkx as nx
import os
from pathlib import Path

def load_all_tiles()->dict:
    """Build a dictionary of tiles with relevenat data"""
    tile_dic = {}
    print('Using the following files:')
    for file in os.listdir(md.tiles_folder):
        print(file)
        if file.lower().endswith('.png'):
            _, tile_id, zoom, lat, lon = file.removesuffix(".png").split('_')
            tile_dic.update({tile_id : {"zoom":zoom, "lat":lat, "lon":lon, "name":file}})
    return tile_dic

def build_image_from_tiles(tile_dic:dict)->None:
    """build a full sized image from thiles"""
    """for tile_id, (zoom, lon, lat, file) in tile_dic.items():
        mimage.imread(os.path.join(md.tiles_folder, file))"""
    Graph = nx.Graph()
    Graph.add_nodes_from(tile_dic)
    nx.set_node_attributes(Graph, tile_dic)
    for home in Graph.nodes.items():
        for neighbor in Graph.nodes.items():
            if home != neighbor:
                if (home[1]["lat"] == neighbor[1]["lat"]) or (home[1]["lon"] == neighbor[1]["lon"]):
                    Graph.add_edge(home[0], neighbor[0])

    print(Graph)
    nx.draw(Graph, with_labels=True, font_weight='bold')
    plt.show()

if __name__ == "__main__":
    tile_dic = load_all_tiles()
    build_image_from_tiles(tile_dic)