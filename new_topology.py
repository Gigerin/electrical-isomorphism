# -*- coding: utf-8 -*-
import networkx
import networkx as nx

from util import *
import matplotlib.patches as patches
import matplotlib
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as image
from dataclasses import fields, asdict
matplotlib.use("TkAgg")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from shapely.geometry import Polygon, MultiPolygon




TRANSISTOR_FILE_NAME = "static/png-clipart-transistor-npn-electronics-electronic-symbol-symbol-miscellaneous-electronics.png"

# showing the layers in matplotlib
transistor_img = image.imread(TRANSISTOR_FILE_NAME)

#TODO добавить повсеместно типизацию
def two_comp_intersect(comp1, comp2):
    """
    check if two components are intersected
    :param comp1:
    :param comp2:
    :return:
    """
    comp1 = asdict(comp1).values() #TODO неэффективно каждый раз все в словарь переводить.
    comp2 = asdict(comp2).values()
    for poly1 in comp1:
        for poly2 in comp2:
            if poly1.intersects(poly2) or poly2.intersects(poly1):
                return True
    return False


def convert_dict_to_graph(dict):
    """
    Конвертируем список компонентов в граф
    :param dict:
    :return:
    """
    graph = networkx.Graph()
    for key in dict.keys():
        collective = dict[key]
        collective_dict = asdict(collective).values() #TODO ОЧЕРЕДНОЙ КОСТЫЛЬ БЛЯТЬ
        collective_poly = MultiPolygon(collective_dict)
        centroid = collective_poly.centroid
        graph.add_node(key, pos = [centroid.x, centroid.y])
    for comp1 in dict.keys():
        for comp2 in dict.keys():
            if comp1 == comp2: #чек если одна и та же компонента(петли не хотим)
                continue
            if 'contact' not in comp1 and 'contact' not in comp2:
                #если не контакт скипаем
                #pass
                continue

            if two_comp_intersect(dict[comp1], dict[comp2]):#TODO некоторые пары мы проходим дважды, неэффективно
                graph.add_edge(comp1, comp2)
                graph.add_edge(comp2, comp1)
    return graph

def draw_schema(data):
    num_keys = 10000
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    colors = cm.viridis(np.linspace(0, 1, num_keys))
    color_dict = {key: color for key, color in zip(data.keys(), colors)}
    for key in data.keys():
        ver = data[key]
        vertic = asdict(ver).values()
        for vertices in vertic:
            xy = list(vertices.exterior.coords)
            if str(key)[:2] != "SP":
                polygon = patches.Polygon(
                    xy,
                    closed=True,
                    linewidth=1,
                    edgecolor=color_dict[key],
                    facecolor="none",
                )
            else:
                polygon = patches.Polygon(
                    xy, closed=True, linewidth=1, edgecolor="red", facecolor="none"
                )
            ax.add_patch(polygon)
    ax.set_xlim(-10000, 10000)
    ax.set_ylim(-10000, 10000)

    # Show the plot
    plt.show()




file_name = input("Please enter name of file(blank for default):")
if not file_name:
    file_name = "sum.cif"
data = read_file_to_list(file_name)
print("DATA")
print(data)
draw_schema(data)
print(data.keys())
graph1 = convert_dict_to_graph(data)
graph2 = convert_dict_to_graph(data)
graph2.add_edge("r_contact114", "m_contact135")
print(networkx.vf2pp_is_isomorphic(graph1, graph2))
networkx.draw(graph1, nx.get_node_attributes(graph1, 'pos'), with_labels = True)
plt.show()