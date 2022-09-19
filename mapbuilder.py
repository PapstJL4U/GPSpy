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
            _, tile_id, zoom, north, west, south, east = file.removesuffix(".png").split('_')
            tile_dic.update({tile_id : {"zoom":int(zoom), "north":float(north), "west":float(west),\
                "south":float(south), "east":float(east), "name":file}})
    return tile_dic

def build_tile_graph(tile_dic:dict)->None:
    """build a full sized image from thiles"""
    Graph = nx.Graph()
    Graph.add_nodes_from(tile_dic)
    nx.set_node_attributes(Graph, tile_dic)
    for home in Graph.nodes.items():
        for neighbor in Graph.nodes.items():
            if home != neighbor:
                if ((home[1]["north"] == neighbor[1]["south"])\
                    or (home[1]["south"] == neighbor[1]["north"]))\
                    and (home[1]["east"] == neighbor[1]["east"]):
                        Graph.add_edge(home[0], neighbor[0], orientation="lat")

                if ((home[1]["west"] == neighbor[1]["east"])\
                    or (home[1]["east"] == neighbor[1]["west"]))\
                    and (home[1]["north"] == neighbor[1]["north"]):
                        Graph.add_edge(home[0], neighbor[0], orientation="lon")
    print(Graph)
    nx.draw(Graph, with_labels=True, font_weight='bold',)
    plt.show()

if __name__ == "__main__":
    tile_dic = load_all_tiles()
    build_tile_graph(tile_dic)