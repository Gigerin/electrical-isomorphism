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
import time


def read_file(name):
    result = {}
    number = 0
    with open(name, "r") as file:
        program_name = file.readline()
        while True:
            line_one = file.readline()
            if not line_one:
                break
            curr_line = line_one.split()
            if len(curr_line):
                if curr_line[0] == "L":
                    layer_name = str(curr_line[1].replace(";",""))+str(number)
                    line_two = file.readline().split()
                    if line_two[0] == "P":
                        if layer_name not in result.keys():
                            result[layer_name] = []
                        polygon = []
                        for i in range(1, len(line_two), 2):
                            polygon.append((int(line_two[i].replace(";", "")), int(line_two[i+1].replace(";", ""))))
                        if len(polygon) % 2 != 0:
                            polygon.insert(len(polygon), (polygon[len(polygon)-1][0], polygon[0][1]))
                        result[layer_name] = Polygon(polygon)
                    if line_two[0] == "4N":
                        if layer_name not in result.keys():
                            result[layer_name] = []
                        result[layer_name] = [line_two[1], int(line_two[2]), int(line_two[3].replace(";",""))]
                        line_three = file.readline()
                if curr_line[0] == "DS":
                    continue
            number = number + 1
    return result

def get_connections(initial_polygon: Polygon, polygon_layer:str, data:dict):
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
            polygon = data[layer]
            if polygon.contains(initial_polygon):
                result.append(layer)
    return result


#showing the layers in matplotlib
def show_circuit(data):
    num_keys = 10000
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    colors = cm.viridis(np.linspace(0, 1, num_keys))
    color_dict = {key: color for key, color in zip(data.keys(), colors)}
    for key in data.keys():
        vertices =  data[key]
        xy = list(vertices.exterior.coords)
        if str(key)[0] != "C":
            polygon = patches.Polygon(xy, closed=True, linewidth=1, edgecolor=color_dict[key], facecolor='none')
        else:
            polygon = patches.Polygon(xy, closed=True, linewidth=1, edgecolor="red", facecolor='none')
        ax.add_patch(polygon)
    ax.set_xlim(-10000, 10000)
    ax.set_ylim(-10000, 10000)
    plt.show()


def convert_data_to_graph(data):
    """
    Переводит словарь многоугольников в граф.
    :param data: входной словарь
    :return: граф
    """
    graph = networkx.Graph()
    for key in data.keys():
        polygon = data[key]
        graph.add_node(key, layer = polygon)
        if str(key)[0] == "C":
            connections = get_connections(polygon, key, data)
            for connection in connections:
                graph.add_edge(key, connection)
    return graph

data = read_file("sum.cif")
transistors = {k: data.pop(k) for k in list(data.keys()) if any(k.startswith(prefix) for prefix in ["TSP", "TM1", "TM2", "TSN", "CW", "M2A"])}

graph = convert_data_to_graph(data)

graph_2 = graph.copy()
print(len(data.keys()))
start = time.time()
print(networkx.vf2pp_is_isomorphic(graph, graph_2))
end = time.time()

print(end-start)

print(len(data.keys()))
show_circuit(data)

