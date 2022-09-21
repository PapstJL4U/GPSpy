"""Loads the tiles, builds a graph and finds the boundaries of the map"""
from math import cos
from PIL import Image as pimage
from PIL import ImageDrawing as pimdraw
import pandas as pd
from matplotlib import image as mimage
from matplotlib import pyplot as plt
import my_data as md
import smopy as sm
import networkx as nx
import os
import so_networkx as so
from pathlib import Path
class TileGraph():

    def __init__(self):
        
        self.tile_dic = self.load_all_tiles()       
        self.Graph = self.build_tile_graph(self.tile_dic)
        self.max_lat, self.max_lon, self.min_lat, self.min_lon = self.map_boundaries(self.tile_dic)
        self.average_lat, self.average_lon = self.avg_tile_size_degree(self.tile_dic)
        self.visited = []
        
    def load_all_tiles(self)->dict:
        """Build a dictionary of tiles with relevant data"""
        local_tile_dic = {}
        print('Using the following files:')
        for file in os.listdir(md.tiles_folder):
            print(file)
            if file.lower().endswith('.png'):
                _, tile_id, zoom, north, west, south, east = file.removesuffix(".png").split('_')
                local_tile_dic.update({tile_id : {"zoom":int(zoom), "north":float(north), "west":float(west),\
                    "south":float(south), "east":float(east), "name":file}})
        return local_tile_dic

    def build_tile_graph(self, tile_dic:dict)->nx.Graph:
        """build a full sized image from thiles"""
        Graph = nx.DiGraph()
        Graph.add_nodes_from(tile_dic)
        nx.set_node_attributes(Graph, tile_dic)
        for home in Graph.nodes.items():
            for neighbor in Graph.nodes.items():
                if home != neighbor:
                    if (home[1]["north"] == neighbor[1]["south"])\
                        and (home[1]["east"] == neighbor[1]["east"]):
                            Graph.add_edge(neighbor[0], home[0], orientation="South")
                    if (home[1]["south"] == neighbor[1]["north"])\
                        and (home[1]["east"] == neighbor[1]["east"]):
                            Graph.add_edge(neighbor[0], home[0], orientation="North")
                    
                    if (home[1]["west"] == neighbor[1]["east"])\
                        and (home[1]["north"] == neighbor[1]["north"]):
                            Graph.add_edge(neighbor[0], home[0], orientation="East")
                    if (home[1]["east"] == neighbor[1]["west"])\
                        and (home[1]["north"] == neighbor[1]["north"]):
                            Graph.add_edge(neighbor[0], home[0], orientation="West")
        print(Graph.edges)
        pos = nx.spring_layout(Graph)
        nx.draw(Graph, with_labels=True, font_weight='bold', pos=pos, connectionstyle='arc3, rad = 0.5')
        edge_labels = nx.get_edge_attributes(Graph,'orientation')
        #nx.draw_networkx_edge_labels(Graph, pos, edge_labels = edge_labels)
        so.my_draw_networkx_edge_labels(Graph, pos, edge_labels = edge_labels, rad=0.5)
        #plt.show()
        return Graph

    def map_boundaries(self, tile_dic:dict)->tuple:
        """return the boundaries of the map based on the used tiles
        returns (max_lat, max_lon, min_lat, min_lon)"""
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

    def avg_tile_size_degree(self, tile_dict:dict)->int:
        """returns the average tile size of all tiles in the dictionary
        in degrees. Returns average_lat, average_lon"""
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
    
    def set_coordinates(self, origin=None, myself=None):
        """find the coordinates based on the origin"""
        if myself not in self.visited:
            if origin is None:
                self.tile_dic[myself].update({"X": 0, "Y": 0})
            else:
                where_from = self.Graph[myself][origin]["orientation"]
                
                X = self.tile_dic[origin]["X"]
                Y = self.tile_dic[origin]["Y"]

                if where_from == "North":
                    Y = self.tile_dic[origin]["Y"]-1   
                elif where_from =="South":
                    Y = self.tile_dic[origin]["Y"]+1
                elif where_from =="East":
                    X = self.tile_dic[origin]["X"]-1
                elif where_from == "West":
                    X = self.tile_dic[origin]["X"]+1
                self.tile_dic[myself].update({"X": X, "Y": Y})

            self.visited.append(myself)
            for nbs in nx.neighbors(self.Graph, myself):
                self.set_coordinates(myself, nbs)

    def set_positive_coordinates(self):
        smallest_x,smallest_y = 1, 1
        for _,tile in self.tile_dic.items():
            if tile["X"]<=smallest_x:
                smallest_x = tile["X"]
            if tile["Y"]<=smallest_y:
                smallest_y = tile["Y"]
        print(smallest_x, smallest_y)
        set_x = abs(smallest_x)
        set_y = abs(smallest_y)
        for _,tile in self.tile_dic.items():
            tile["X"] += set_x
            tile["Y"] += set_y

def drawing(self, mla, mlo, tile_dic:dict)->None:
    """draw an image with all tiles"""
    tile_dim = 256
    target_img = pimage.new('RGBA', (tile_dim*mlo, tile_dim*mla), (192,192,192,0))

if __name__ == "__main__":
    TG  = TileGraph()
    #Graph:nx.Graph = TG.build_tile_graph(TG.tile_dic)   
    mla = int(round((TG.max_lat-TG.min_lat) / TG.average_lat,0))
    mlo = int(round((TG.max_lon-TG.min_lon) / TG.average_lon,0))
    
    TG.set_coordinates(None, '0')
    TG.set_positive_coordinates()