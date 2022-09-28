"""Visualize my way to *******"""
import pandas as pd
from matplotlib import image as mimage
from matplotlib import pyplot as plt
import data.my_data as md
import mapbuild.mapbuilder as mp
import smopy as sm
import os
import pathlib as Path

def detailed_tiles(locations:tuple = None, zoom=15)->set:
    """find the unique list of tiles for all locations"""
    tile_list = [None]*len(locations)
    for i, tile in enumerate(locations):
        tile_list[i] = sm.deg2num(tile[0], tile[1],zoom)
    print(set(tile_list), len(set(tile_list)))
    return (set(tile_list))

def load_all_tiles(path_to_gps_file:str, tile_list:list[tuple], zoom:int=15)->None:
    """load all tiles"""
    for i,tile in enumerate(tile_list):
        #find the center of a tile
        lat, lon = sm.num2deg(tile[0]+0.5, tile[1]+0.5, zoom)

        #get the boundaries of the tile
        north, west = sm.num2deg(tile[0]+0, tile[1]+0, zoom)
        south, east = sm.num2deg(tile[0]+1, tile[1]+1, zoom)

        #round all to 5 digits
        north, west, south, east = [round(x, 5) for x in [north, west, south, east]]

        #get the single tile based on the center point to allow maximum zoom
        mao = sm.Map(lat, lon, z=zoom)
        #save the tile with the boudaries and zoom
        pathy:Path = Path.Path(path_to_gps_file)
        mao.save_png(pathy.joinpath(f"Tile_{i}_{zoom}_{north}_{west}_{south}_{east}.png"))

def plot_my_path(file_path:str = "None", only_location:tuple = None, df:pd.DataFrame = None)->str:
    """do all the loading, plotting and saving files"""

    #find the latitude and longitude boundaries of the gps trail
    left, right= min(df['lon']), max(df['lon'])
    bottom, top = min(df['lat']), max(df['lat'])
    box = (bottom, left, top, right) 
    #point = sm.POINT if you want to define the boundaries yourself.

    #load current map from openstreetmaps
    my_map = sm.Map(box, z=15, margin=0.00)
    image = file_path +".png"
    my_map.save_png(image)
    #convert real gps data to pixels on the map
    location_on_image = list(map(my_map.to_pixels, only_location))
    
    #matplotlib needs x and y coordinates as distinct list and as integers
    # x = list of only x coordinates
    # y = list of only y coordinates
    y = [0]*len(location_on_image)
    x = [0]*len(location_on_image)
    for i,pxl in enumerate(location_on_image):
        x[i] =  int(pxl[0])
        y[i] =  int(pxl[1])

    data = mimage.imread(image)
    plt.plot(x,y,color="blue", linewidth=1)
    plt.axis('off')
    plt.imshow(data)
    plt.savefig(file_path+"_final.png", dpi=600)

    return file_path+"_final.png"

def plot_my_mapbuilder(path_to_tiles_folder:str,only_location:tuple = None, df:pd.DataFrame = None)->str:
    """do all the loading, plotting and saving files"""

    #find the latitude and longitude boundaries of the gps trail
    left, right= min(df['lon']), max(df['lon'])
    bottom, top = min(df['lat']), max(df['lat'])
    point = (bottom, left, top, right) 

    #generate the graph from the tiles_folder
    TG = mp.TileGraph(Path.Path(path_to_tiles_folder))
    #The graph is relative and needs Grid-like coordinates
    TG.set_coordinates(None, '0')
    #Coordinates can be positive and negative, make them all start postive
    TG.set_positive_coordinates()
    #finally draw the image and save it, return path to image
    pathy = TG.drawing()

    #convert real gps data to pixels on the map
    location_on_image = list(map(TG.to_pixels, only_location))
    #load the detailed image
    data = mimage.imread(pathy)

    #matplotlib needs x and y coordinates as distinct list and as integers
    # x = list of only x coordinates
    # y = list of only y coordinates    
    y = [0]*len(location_on_image)
    x = [0]*len(location_on_image)
    for i,pxl in enumerate(location_on_image):
        x[i] =  int(pxl[0])
        y[i] =  int(data.shape[0] - pxl[1]) #invert coordinates, because its and image

    plt.plot(x,y,color="red", linewidth=0.5)
    plt.axis('off')
    plt.imshow(data)
    plt.savefig(os.path.join(path_to_tiles_folder,"mapbuilder_final.png"), dpi=600)
    return 

def single_tile_gps(path_to_gps_file:str="/")->str:
        #read gps data from file and
    # filter to only get latitude and longitude
    df = pd.read_csv(path_to_gps_file+'.csv', sep=',')
    only_location = tuple(zip(df['lat'],df['lon']))
    path_to_image = plot_my_path(path_to_gps_file, only_location, df)
    #plot a path within a single tile
    return path_to_image

def multi_tile_gps(path_to_gps_file:str="/")->str:
        #read gps data from file and
    # filter to only get latitude and longitude
    df = pd.read_csv(path_to_gps_file+'.csv', sep=',')
    only_location = tuple(zip(df['lat'],df['lon']))
    
    unique_tiles = detailed_tiles(only_location, zoom=15)
    #download all tiles if not yet downloaded
    load_all_tiles(path_to_gps_file,unique_tiles, zoom=15)

    path_to_image = plot_my_mapbuilder(path_to_gps_file, only_location, df)
    #plot a path within a single tile
    return path_to_image