"""Visualize my way to *******"""
import pandas as pd
from matplotlib import image as mimage
from matplotlib import pyplot as plt
import my_data as md
import smopy as sm
import mapbuilder as mp

def detailed_tiles(locations:tuple = None, zoom=15)->set:
    """find the unique list of tiles for all locations"""
    tile_list = [None]*len(locations)
    for i, tile in enumerate(locations):
        tile_list[i] = sm.deg2num(tile[0], tile[1],zoom)
    print(set(tile_list), len(set(tile_list)))
    return (set(tile_list))

def load_all_tiles(tile_list:list[tuple], zoom=15):
    """load all tiles"""
    for i,tile in enumerate(tile_list):
        lat, lon = sm.num2deg(tile[0]+0.5, tile[1]+0.5, zoom)
        north, west = sm.num2deg(tile[0]+0, tile[1]+0, zoom)
        south, east = sm.num2deg(tile[0]+1, tile[1]+1, zoom)

        #round all to 5 digits
        north, west, south, east = [round(x, 5) for x in [north, west, south, east]]

        mao = sm.Map(lat, lon, z=zoom)
        mao.save_png(md.tiles_folder.joinpath(f"Tile_{i}_{zoom}_{north}_{west}_{south}_{east}.png"))

def plot_my_path(only_location:tuple = None, df:pd.DataFrame = None)->None:
    """do all the loading, plotting and saving files"""

    #find the latitude and longitude boundaries of the gps trail
    left, right= min(df['lon']), max(df['lon'])
    bottom, top = min(df['lat']), max(df['lat'])
    point = (bottom, left, top, right) 
    #point = sm.POINT if you want to define the boundaries yourself.

    #load current map from openstreetmaps
    my_map = sm.Map(point, z=15, margin=0.00)
    my_map.save_png(md.folder.joinpath("auto_map.png"))
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

    data = mimage.imread(md.map_png)
    plt.plot(x,y,color="blue", linewidth=1)
    plt.axis('off')
    plt.imshow(data)
    plt.savefig(md.folder.joinpath("auto_result.png"), dpi=600)
    plt.show()

def plot_my_mapbuilder(only_location:tuple = None, df:pd.DataFrame = None)->None:
    """do all the loading, plotting and saving files"""

    #find the latitude and longitude boundaries of the gps trail
    left, right= min(df['lon']), max(df['lon'])
    bottom, top = min(df['lat']), max(df['lat'])
    point = (bottom, left, top, right) 
    #point = sm.POINT if you want to define the boundaries yourself.

    #generate and load map from mapbuilder
    TG = mp.TileGraph()
    TG.set_coordinates(None, '0')
    TG.set_positive_coordinates()
    pathy = TG.drawing()
    #convert real gps data to pixels on the map
    location_on_image = list(map(TG.to_pixels, only_location))
    
    #matplotlib needs x and y coordinates as distinct list and as integers
    # x = list of only x coordinates
    # y = list of only y coordinates
    y = [0]*len(location_on_image)
    x = [0]*len(location_on_image)
    for i,pxl in enumerate(location_on_image):
        x[i] =  int(pxl[0])
        y[i] =  int(pxl[1])

    data = mimage.imread(pathy)
    plt.plot(x,y,color="blue", linewidth=1)
    plt.axis('off')
    plt.imshow(data)
    plt.savefig(md.folder.joinpath("mapbuilder_result.png"), dpi=600)
    plt.show()

if __name__ == "__main__":
    #read gps data from file and
    # filter to only get latitude and longitude
    df = pd.read_csv(md.work_csv, sep=',')
    only_location = tuple(zip(df['lat'],df['lon']))
    unique_tiles = detailed_tiles(only_location, zoom=15)
    #load_all_tiles(unique_tiles, zoom=15)
    #plot_my_path(only_location, df)
    plot_my_mapbuilder(only_location, df)