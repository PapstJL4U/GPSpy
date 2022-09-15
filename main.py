"""Visualize my way to *******"""
import pandas as pd
from matplotlib import image as mimage
from matplotlib import pyplot as plt
import my_data as md
import smopy as sm

def detailed_tiles(locations:tuple = None, zoom=13)->None:
    """find more detailed tiles"""
    tile_list = [None]*len(locations)
    for i, tile in enumerate(locations):
        tile_list[i] = sm.deg2num(tile[0], tile[1],zoom)
    
    print(set(tile_list), len(set(tile_list)))

def plot_my_path(only_location:tuple = None)->None:
    """do all the loading, plotting and saving files"""

    #find the latitude and longitude boundaries of the gps trail
    left, right= min(df['lon']), max(df['lon'])
    bottom, top = min(df['lat']), max(df['lat'])
    point = (top, left, bottom, right) 
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
        y[i] =  int(pxl[0])
        x[i] =  int(pxl[1])

    data = mimage.imread(md.map_png)
    plt.plot(y,x,color="blue", linewidth=1)
    plt.axis('off')
    plt.imshow(data)
    plt.savefig(md.folder.joinpath("auto_result.png"), dpi=600)
    plt.show()

if __name__ == "__main__":
    #read gps data from file and
    # filter to only get latitude and longitude
    df = pd.read_csv(md.work_csv, sep=',')
    only_location = tuple(zip(df['lat'], df['lon']))
    detailed_tiles(only_location, zoom=15)
    detailed_tiles(only_location, zoom=13)
    detailed_tiles(only_location, zoom=5)
    #plot_my_path(only_location)