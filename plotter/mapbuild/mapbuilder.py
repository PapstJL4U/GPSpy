"""Loads the tiles, builds a graph and generates and image with the tiles"""
import networkx as nx
import os
from PIL import Image as pimage
from matplotlib import pyplot as plt
if __name__ == '__main__':
    import so_networkx as so
else:
    import mapbuild.so_networkx as so
from smopy import deg2num
from pathlib import Path

class TileGraph():
    """The instance of the a graph-. Contains the graph itself, a dictionary of Tiles used in the graph,
        zoom level, boundaries, and options to draw an image"""
    
    def __init__(self, path_to_tiles:Path=None):
        """Creating an TileGraph instance generates most of it based on a dictionary of Tiles"""
        #path to find the images of the tiles
        self.tiles_folder = path_to_tiles
        #this dictionary represents all the tiles images as easily accessable entries
        self.tile_dic = self.load_all_tiles()
        #The networkx Graph representation of the tiles
        self.Graph = self.build_tile_graph(self.tile_dic)
        #Max values of the edges from al tiles. All tiles can be placed within theses boundaries
        self.max_lat, self.max_lon, self.min_lat, self.min_lon = self.map_boundaries(self.tile_dic)
        #Zoom factor of this map
        self.zoom = self.tile_dic["0"]["zoom"]
        
        #Pixel version of the above gps coordinates to draw them within the correct boundaries
        self.min_x, self.min_y  = deg2num(self.min_lat, self.min_lon, self.zoom, do_round=False) 
        self.max_x, self.max_y = deg2num(self.max_lat, self.max_lon, self.zoom, do_round=False)

        #get the average height and width of a tile in lat/lat
        self.average_lat, self.average_lon = self.avg_tile_size_degree(self.tile_dic)
        #to stop endless loops when building the graph we remember where we were
        #initialize for nothing
        self.visited = []

        #tile size in pixel, tiles are quadratic
        self.tile_dim = 256
        #size of the map in tiles
        #i.e a map of 3 horizonatal tiles and 5 vertical tiles 
        #has a size of mla=5, mlo=3, 3 by 5 tiles
        self.mla = int(round((self.max_lat-self.min_lat) / self.average_lat,0))
        self.mlo = int(round((self.max_lon-self.min_lon) / self.average_lon,0))
        
    def load_all_tiles(self)->dict:
        """Build a dictionary of tiles with relevant data
        return: dictionary"""
        local_tile_dic = {}
        print('Using the following files:')
        for file in os.listdir(self.tiles_folder):
            if file.lower().endswith('.png') and file.lower().startswith('tile'):
                _, tile_id, zoom, north, west, south, east = file.removesuffix(".png").split('_')
                local_tile_dic.update({tile_id : {"zoom":int(zoom), "north":float(north), "west":float(west),\
                    "south":float(south), "east":float(east), "name":file}})
        return local_tile_dic

    def build_tile_graph(self, tile_dic:dict)->nx.Graph:
        """build a full sized image from thiles
        return: nx.DiGraph"""
        Graph = nx.DiGraph()
        Graph.add_nodes_from(tile_dic)
        nx.set_node_attributes(Graph, tile_dic)
        #Go through each tile and find edges to every other tile
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

        #create dummy tiles for tiles that have no orthoginal neigbours, but hopefully diagonal neigbours
        for node in Graph.nodes.items():
            if Graph.degree[node[0]]==0:
                self.set_dummies(node)
        # The module can be used alone
        # This part is mainly for debugging
        if __name__ == "__main__":
            pos = nx.spring_layout(Graph)
            nx.draw(Graph, with_labels=True, font_weight='bold', pos=pos, connectionstyle='arc3, rad = 0.5')
            edge_labels = nx.get_edge_attributes(Graph,'orientation')
            so.my_draw_networkx_edge_labels(Graph, pos, edge_labels = edge_labels, rad=0.5)
            plt.show()

        return Graph

    def map_boundaries(self, tile_dic:dict)->tuple:
        """return the boundaries of the map based on the used tiles
        return: (max_lat, max_lon, min_lat, min_lon)"""
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
        in degrees. 
        Return: average_lat, average_lon"""
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
    
    def set_coordinates(self, origin:str=None, myself:str=None)->None:
        """find the coordinates based on the origin"""

        #Stop loops by not repeating oneself
        if myself not in self.visited:
            if origin is None:
                self.tile_dic[myself].update({"X": 0, "Y": 0})
            else:
                where_from = self.Graph[myself][origin]["orientation"]
                
                X = self.tile_dic[origin]["X"]
                Y = self.tile_dic[origin]["Y"]

                if where_from == "North":
                    Y = self.tile_dic[origin]["Y"]+1   
                elif where_from =="South":
                    Y = self.tile_dic[origin]["Y"]-1
                elif where_from =="East":
                    X = self.tile_dic[origin]["X"]-1
                elif where_from == "West":
                    X = self.tile_dic[origin]["X"]+1
                self.tile_dic[myself].update({"X": X, "Y": Y})

            self.visited.append(myself)
            for nbs in nx.neighbors(self.Graph, myself):
                self.set_coordinates(myself, nbs)

    def set_positive_coordinates(self):
        """shift the coordinates into the positive real to make
        the tiles easy to draw"""

        #find the smallest possible value for x and y
        smallest_x,smallest_y = 1, 1
        for _,tile in self.tile_dic.items():
            if tile["X"]<=smallest_x:
                smallest_x = tile["X"]
            if tile["Y"]<=smallest_y:
                smallest_y = tile["Y"]
        
        #add the absolute value to every tiles coordinates
        #to shift it by that amount
        set_x = abs(smallest_x)
        set_y = abs(smallest_y)
        for _,tile in self.tile_dic.items():
            tile["X"] += set_x
            tile["Y"] += set_y

    def drawing(self, name:str=None)->Path:
        """draw an image with all tiles
        Return: Path.Path"""
        #draw a base image with the dimensions: number of tiles * tile size
        target_img = pimage.new('RGBA', (self.tile_dim*self.mlo, self.tile_dim*self.mla), (192,192,192,0))
        
        #draw every single tile
        for _, tile in self.tile_dic.items():
            image = pimage.open(self.tiles_folder.joinpath(tile["name"]), 'r')
            X = tile["X"]
            Y = tile["Y"]
            target_img.paste(image, (X*self.tile_dim, Y*self.tile_dim))

        z = str(self.tile_dic["0"]["zoom"])
        if name is None:
            name = "Combined_Tiles_Zoom_"
        pathy:Path = self.tiles_folder.joinpath(name+z+"_final.png")
        target_img.save(pathy)
        
        return pathy

    def to_pixels(self, lat_lon:tuple)->float:
        """Convert lat and lon coordinates to pixels based on the image
        Return: px,py"""
        lat, lon = lat_lon
        zoom = self.zoom
        x,y = deg2num(lat, lon, zoom=zoom, do_round=False)
        xx,yy = deg2num(self.min_lat, self.min_lon, zoom=zoom, do_round=False)
        px = abs(x - self.min_x) * self.tile_dim
        py = abs(y - self.min_y) * self.tile_dim
        
        return px,py

    def set_dummies(self, node):

        _ele = len(self.tile_dic)
        _s = node[1]["south"]
        _n = node[1]["north"]
        _w = node[1]["west"]
        _e = node[1]["east"]
        _z = node[1]["zoom"]
        north_dummy = {_ele+1 : {"south": _n, "north": _n, "west": _w, "east": _e, "zoom": _z}}
        south_dummy = {_ele+2 : {"north": _s, "south": _s, "west": _w, "east": _e, "zoom": _z}}
        east_dummy = {_ele+1 : {"south": _s, "north": _n, "west": _e, "east": _e, "zoom": _z}}
        west_dummy = {_ele+1 : {"south": _s, "north": _n, "west": _w, "east": _w, "zoom": _z}}
        self.tile_dic.update(north_dummy)
        self.tile_dic.update(south_dummy)
        self.tile_dic.update(east_dummy)
        self.tile_dic.update(west_dummy)


if __name__ == "__main__":
    TG  = TileGraph(Path.home().joinpath(r"Documents\gps\tiles"))   
    TG.set_coordinates(None, '0')
    TG.set_positive_coordinates()
    TG.drawing()