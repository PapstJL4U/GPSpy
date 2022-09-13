from pathlib import Path
import csv

home:Path = Path.home()
folder:Path = home.joinpath(r"Documents\gps")
first_csv:Path = home.joinpath(r"Documents\gps\20220905.csv")
second_csv:Path = home.joinpath(r"Documents\gps\20220907.csv")
work_csv:Path = home.joinpath(r"Documents\gps\20220912.csv")

first_gpx:Path = home.joinpath(r"Documents\gps\20220905.gpx")
second_gpx:Path = home.joinpath(r"Documents\gps\20220907.gpx")

osm_dimension:Path = home.joinpath(r"Documents\gps\osm_dimension.txt")
map_png:Path = home.joinpath(r"Documents\gps\auto_map.png")
map_osm:Path = home.joinpath(r"Documents\gps\map.osm")
map_hand:Path = home.joinpath(r"Documents\gps\hand_map.png")

#to load a map from openstreetmaps we need the boundaries
#of the map
#they are not accurate
TOP:float = 0.0
LEFT:float = 0.0
BOTTOM:float = 0.0
RIGHT:float = 0.0

#load boundries from a file elsewere on the computer
#we don't want to dox ourself, do we?
with open(osm_dimension, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile, skipinitialspace=True)
    for row in reader:
        TOP = float(row["top"])
        LEFT = float(row["left"])
        BOTTOM = float(row["bottom"])
        RIGHT = float(row["right"])
    del(reader)
    del(csvfile)
    del(row)

POINT = (TOP, LEFT, BOTTOM, RIGHT)

if __name__ == "__main__":
    for entry in list(locals().values())[-15:]:
        print(entry)