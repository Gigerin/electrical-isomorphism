from dataclasses import dataclass

import itertools
import numpy as np
import networkx
import matplotlib.patches as patches
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from shapely.geometry import Polygon


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

def check_connections(initial_polygon: Polygon, polygon_layer:str, data:dict):
    """
    :param initial_polygon: Исходный квадратик контактный
    :param polygon_layer: Слой квадратика
    :param data: данные о всех слоях
    :return: возвращает, между какими слоями и изначальным слоем надо дать ребро, список
    """
    result = []
    for layer in data.keys():
        if layer == polygon_layer:
            continue
        else:
            polygons = data[layer]
            for polygon in polygons:
                if polygon.contains(initial_polygon):
                    print(layer, polygon)
                    result.append(polygon)
    return result




data = read_file("sum.cif")

transistors = {k: data.pop(k) for k in ["TSP", "TM1", "TM2", "TSN"] if k in data}
data.pop("CW")
data.pop("M2A")
num_keys = len(data.keys())
colors = cm.viridis(np.linspace(0, 1, num_keys))

# Generate the dictionary
color_dict = {key: color for key, color in zip(data.keys(), colors)}
# Create a new figure and axis


number = 0


#showing the layers in matplotlib
def show_circuit(data):
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    for key in data.keys():
        for vertices in data[key]:
            xy = list(vertices.exterior.coords)
            if str(key)[0] != "C":
                polygon = patches.Polygon(xy, closed=True, linewidth=1, edgecolor=color_dict[key], facecolor='none')
            else:
                polygon = patches.Polygon(xy, closed=True, linewidth=1, edgecolor="red", facecolor='none')

            ax.add_patch(polygon)
    ax.set_xlim(-10000, 10000)
    ax.set_ylim(-10000, 10000)
    plt.show()


graph_1 = networkx.Graph()

#converting everything to a graph
for key in data.keys():
    num = 0
    if key in ["TSP", "TM1", "TM2", "TSN"]:
        continue
    for polygon in data[key]:
        try:
            graph_1.add_node(str(key)+str(num), layer = polygon)
            check_connections()
        except Exception as e:
            print(str(key)+str(num), polygon, e)
        num = num+1

for key in data.keys():
    pass

show_circuit(data)

print(data)

