from dataclasses import dataclass

import itertools
import numpy as np
import networkx
import matplotlib.patches as patches
import matplotlib
from matplotlib.offsetbox import (OffsetImage, AnnotationBbox)
import matplotlib.image as image
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from shapely.geometry import Polygon

TRANSISTOR_FILE_NAME = "png-clipart-transistor-npn-electronics-electronic-symbol-symbol-miscellaneous-electronics.png"

def read_file(name):
    result = {}
    with open(name, "r") as file:
        program_name = file.readline()
        while True:
            line_one = file.readline()
            if not line_one:
                break
            curr_line = line_one.split()
            if len(curr_line):
                if curr_line[0] == "L":
                    layer_name = curr_line[1].replace(";","")
                    line_two = file.readline().split()
                    if line_two[0] == "P":
                        if layer_name not in result.keys():
                            result[layer_name] = []
                        polygon = []
                        for i in range(1, len(line_two), 2):
                            polygon.append((int(line_two[i].replace(";", "")), int(line_two[i+1].replace(";", ""))))
                        result[layer_name].append(Polygon(polygon))
                    if line_two[0] == "4N":
                        if layer_name not in result.keys():
                            result[layer_name] = []
                        result[layer_name].append([line_two[1], int(line_two[2]), int(line_two[3].replace(";",""))])
                        line_three = file.readline()
                if curr_line[0] == "DS":
                    continue
    return result



data = read_file("sum.cif")
print(data)
print(data.keys())

num_keys = len(data.keys())
colors = cm.viridis(np.linspace(0, 1, num_keys))

# Generate the dictionary
color_dict = {key: color for key, color in zip(data.keys(), colors)}
# Create a new figure and axis
fig, ax = plt.subplots()
fig.set_size_inches(8, 6)

number = 0
transistor_img = image.imread(TRANSISTOR_FILE_NAME)
for key in data.keys():
    print(key)

    if key in ["TSP", "TM1", "TM2", "TSN"]:
        for vertice in data[key]:
            xycoords = (vertice[1], vertice[2])
            imagebox = OffsetImage(transistor_img, zoom = 0.01)
            ab = AnnotationBbox(imagebox, xycoords, frameon = False)
            ax.add_artist(ab)
            
        number = number + len(data[key])
        print(number)
        continue
    for vertices in data[key]:
        xy = list(vertices.exterior.coords)
        if str(key)[0] != "C":
            polygon = patches.Polygon(xy, closed=True, linewidth=1, edgecolor=color_dict[key], facecolor='none')
        else:
            polygon = patches.Polygon(xy, closed=True, linewidth=1, edgecolor="red", facecolor='none')

        ax.add_patch(polygon)


ax.set_xlim(-10000, 10000)
ax.set_ylim(-10000, 10000)

imagebox = OffsetImage(transistor_img, zoom = 0.01)
ab = AnnotationBbox(imagebox, (-83, -50), frameon = False)
ax.add_artist(ab)
# img = plt.imread(file)
# ax.figure.figimage(img, 6707, 780,
#                    alpha=0, zorder=3)


# Show the plot
plt.show()

graph_1 = networkx.Graph()


for key in data.keys():
    num = 0
    if key in ["TSP", "TM1", "TM2", "TSN"]:
        continue
    for polygon in data[key]:
        try:
            graph_1.add_node(str(num)+str(key), layer = polygon)
        except Exception as e:
            print(str(key)+str(num), polygon, e)
        num = num+1

print(graph_1.nodes)





