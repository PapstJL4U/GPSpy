from typing import Dict
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

def build_tile_graph(tile_dic:dict)->nx.Graph:
    """build a full sized image from thiles"""
    Graph = nx.Graph()
    Graph.add_nodes_from(tile_dic)
    nx.set_node_attributes(Graph, tile_dic)
    for home in Graph.nodes.items():
        for neighbor in Graph.nodes.items():
            if home != neighbor:
                if (home[1]["north"] == neighbor[1]["south"])\
                    and (home[1]["east"] == neighbor[1]["east"]):
                        Graph.add_edge(home[0], neighbor[0], orientation="South")
                if (home[1]["south"] == neighbor[1]["north"])\
                    and (home[1]["east"] == neighbor[1]["east"]):
                        Graph.add_edge(home[0], neighbor[0], orientation="North")
                
                if (home[1]["west"] == neighbor[1]["east"])\
                    and (home[1]["north"] == neighbor[1]["north"]):
                        Graph.add_edge(home[0], neighbor[0], orientation="East")
                if (home[1]["east"] == neighbor[1]["west"])\
                    and (home[1]["north"] == neighbor[1]["north"]):
                        Graph.add_edge(home[0], neighbor[0], orientation="West")
    
    print(Graph)
    nx.draw(Graph, with_labels=True, font_weight='bold',)
    plt.show()
    return Graph
def extreme_values(tile_dic:dict):
    max_lat, max_lon, min_lat, min_lon = -91, -181, 91, 181

    for item in tile_dic.items():
        if item[1]["north"] > max_lon:
            max_lon = item[1]["north"]
        if item[1]["south"] < min_lon:
            min_lon = item[1]["south"]
        if item[1]["east"] < min_lat:
            min_lat = item[1]["east"]
        if item[1]["west"] > max_lat:
            max_lat = item[1]["west"]
    return max_lat, max_lon, min_lat, min_lon

if __name__ == "__main__":
    tile_dic:Dict = load_all_tiles()
    Graph:nx.Graph = build_tile_graph(tile_dic)
    print(extreme_values(tile_dic))