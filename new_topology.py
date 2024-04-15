# -*- coding: utf-8 -*-
import networkx
import networkx as nx

from util import *
import matplotlib.patches as patches
import matplotlib
import matplotlib.image as image
from dataclasses import asdict

matplotlib.use("TkAgg")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from shapely.geometry import MultiPolygon


TRANSISTOR_FILE_NAME = "static/png-clipart-transistor-npn-electronics-electronic-symbol-symbol-miscellaneous-electronics.png"

# showing the layers in matplotlib
transistor_img = image.imread(TRANSISTOR_FILE_NAME)


# TODO добавить повсеместно типизацию
def two_comp_contains(comp1, comp2):
    """
    check if two components are intersected
    :param comp1:
    :param comp2:
    :return:
    """
    comp1 = asdict(
        comp1
    ).values()  # TODO неэффективно каждый раз все в словарь переводить.
    comp2 = asdict(comp2).values()
    for poly1 in comp1:
        for poly2 in comp2:
            if poly1.contains(poly2) or poly2.contains(poly1):
                return True
    return False


def two_comp_intersects(comp1, comp2):
    """
    check if two components are intersected
    :param comp1:
    :param comp2:
    :return:
    """
    comp1 = asdict(
        comp1
    ).values()  # TODO неэффективно каждый раз все в словарь переводить.
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
        collective_dict = asdict(collective).values()  # TODO ОЧЕРЕДНОЙ КОСТЫЛЬ БЛЯТЬ
        collective_poly = MultiPolygon(collective_dict)
        centroid = collective_poly.centroid
        graph.add_node(key, pos=[centroid.x, centroid.y])
    for comp1 in dict.keys():
        for comp2 in dict.keys():
            if comp1 == comp2:  # чек если одна и та же компонента(петли не хотим)
                continue
            if "contact" in comp1 or "contact" in comp2:
                if two_comp_contains(
                    dict[comp1], dict[comp2]
                ):  # TODO некоторые пары мы проходим дважды, неэффективно
                    graph.add_edge(comp1, comp2)
                    graph.add_edge(comp2, comp1)
            if "transistor" in comp1 and "transistor" in comp2:
                if two_comp_intersects(
                    dict[comp1], dict[comp2]
                ):  # TODO некоторые пары мы проходим дважды, неэффективно
                    graph.add_edge(comp1, comp2)
                    graph.add_edge(comp2, comp1)
            if "transistor" in comp1 and "SI_rail" in comp2:
                if two_comp_intersects(
                    dict[comp1], dict[comp2]
                ):  # TODO некоторые пары мы проходим дважды, неэффективно
                    graph.add_edge(comp1, comp2)
                    graph.add_edge(comp2, comp1)
            if "transistor" in comp1 and "Eqwi" in comp2:
                if two_comp_intersects(
                    dict[comp1], dict[comp2]
                ):  # TODO некоторые пары мы проходим дважды, неэффективно
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
node_positions = {
    node: attributes["pos"] for node, attributes in graph1.nodes(data=True)
}

# Use spring layout to automatically position nodes
pos = nx.spring_layout(graph1, pos=node_positions, fixed=node_positions.keys(), k=1000)


color_dict = {
    "SI": "green",
    "M2": "cyan",
    "M1": "yellow",
    "n_transistor": "red",
    "p_transistor": "blue",
}


def find_color_node(node_name):
    for substring, color in color_dict.items():
        if substring in str(node_name):
            return color
    # Default color if no match found
    return "black"


def find_color_edge(edge):
    name1, name2 = edge
    for substring, color in color_dict.items():
        if substring in str(name1) and substring in str(name2):
            return color
        if "rail" in str(name1) or "rail" in str(name2):
            if substring in str(name1) or substring in str(name2):
                return color
    # Default color if no match found
    return "black"


node_colors = [find_color_node(node) for node in graph1.nodes()]
edge_colors = [find_color_edge(edge) for edge in graph1.edges()]

networkx.draw_networkx(
    graph1, pos, node_color=node_colors, edge_color=edge_colors, with_labels=True
)
plt.show()
