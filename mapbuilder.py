"""Loads the tiles, builds a graph and finds the boundaries of the map"""
from math import cos
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

def map_boundaries(tile_dic:dict)->tuple:
    """return the boundaries of the map based on the used tiles"""
    max_lat, max_lon, min_lat, min_lon = -100.0, -200.0, 100.0, 200.0

    for item in tile_dic.items():
        if item[1]["north"] > max_lat:
            max_lat = item[1]["north"]
        if item[1]["south"] < min_lat:
            min_lat = item[1]["south"]
        if item[1]["east"] > max_lon:
            max_lon = item[1]["east"]
        if item[1]["west"] < min_lon:
            min_lon = item[1]["west"]
    return (max_lat, max_lon, min_lat, min_lon)

def avg_tile_size_degree(tile_dict:dict)->int:
    
    list_lat, list_lon = [], []

    for item in tile_dict.items():
        west, east = item[1]["west"], item[1]["east"]
        north, south = item[1]["north"], item[1]["south"]
        distance_lat = abs(north - south)
        distance_lon = abs(east - west)
        list_lat.append(distance_lat)
        list_lon.append(distance_lon)

    average_lat = sum(list_lat)/len(list_lat)
    average_lon = sum(list_lon)/len(list_lon)
    
    return average_lat, average_lon

if __name__ == "__main__":
    tile_dic:dict = load_all_tiles()
    #Graph:nx.Graph = build_tile_graph(tile_dic)
    max_lat, max_lon, min_lat, min_lon = map_boundaries(tile_dic)
    average_lat, average_lon = avg_tile_size_degree(tile_dic)
    mla = round((max_lat-min_lat) / average_lat,0)
    mlo = round((max_lon-min_lon) / average_lon,0)
    print(mla, mlo)