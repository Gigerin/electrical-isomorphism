# -*- coding: utf-8 -*-
import networkx
import matplotlib
import matplotlib.image as image
from util import *
from dataclasses import fields, asdict
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


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
            if poly1.contains(poly2) or poly2.contains(poly1):
                return True
    return False


def convert_dict_to_graph(dict):
    """
    Конвертируем список компонентов в граф
    :param dict:
    :return:
    """
    graph = networkx.Graph()
    graph.add_nodes_from(dict.keys())
    for comp1 in dict.keys():
        for comp2 in dict.keys():
            if comp1 == comp2:
                continue
            if two_comp_intersect(dict[comp1], dict[comp2]):#TODO некоторые пары мы проходим дважды, неэффективно
                graph.add_edge(comp1, comp2)
                graph.add_edge(comp2, comp1)
    return graph
    print(len(graph.edges))




file_name = input("Please enter name of file(blank for default):")
if not file_name:
    file_name = "sum.cif"
data = read_file_to_list(file_name)
print("DATA")
print(data)
print(data.keys())
graph1 = convert_dict_to_graph(data)
graph2 = convert_dict_to_graph(data)
graph2.add_edge("r_contact114", "m_contact135")
print(networkx.vf2pp_is_isomorphic(graph1, graph2))
networkx.draw(graph1, with_labels = True)
plt.show()