"""Visualize my way to *******"""
import pandas as pd
from matplotlib import image as mimage
from matplotlib import pyplot as plt
import my_data as md
import smopy as sm

if __name__ == "__main__":
    #load current map from openstreetmaps
    my_map = sm.Map(md.POINT, z=15, margin=0.00)
    my_map.save_png(md.folder.joinpath("map.png"))
    
    #read gps data from file and
    # filter to only get latitude and longitude
    df = pd.read_csv(md.second_csv, sep=',')
    only_location = tuple(zip(df['lat'], df['lon']))
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
    plt.show()