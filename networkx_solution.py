from dataclasses import dataclass

import itertools
import numpy as np
import networkx
import matplotlib.pyplot as plt


@dataclass
class Transistor:
    name: str
    connections: tuple[str, str, str, str]
    type: str


@dataclass(frozen=True)
class Node:
    name: str
    type: str


def read_file(name):
    result = []
    with open("source/" + name, "r") as file:
        program_name = file.readline()
        while True:
            line = file.readline()
            if not line:
                break
            splitting = line.split()
            name = splitting[0]
            connections = (splitting[1], splitting[2], splitting[3], splitting[4])
            type = splitting[5]
            new_transistor = Transistor(name, connections, type)
            result.append(new_transistor)
    return result


def add_my_edge(graph, node_1, node_2, weight=1):
    if node_2 not in graph.nodes:
        node_2_obj = Node(node_2, type="connection")
        graph.add_node(node_2_obj)
        graph.add_edge(node_2_obj, node_1)
        graph.add_edge(node_1, node_2_obj)
    else:
        graph.add_edge(node_2, node_1)
        graph.add_edge(node_1, node_2)


def data_to_graph(raw_data):
    graph = networkx.Graph()
    for transistor in raw_data:
        node = Node(transistor.name, transistor.type)
        graph.add_node(node)
        for con in transistor.connections:
            add_my_edge(graph, node, con)
    return graph


# читаем данные, переводим их в нужные типы
raw_data_1 = read_file("source.txt")
# читаем данные, переводим их в нужные типы
raw_data_2 = read_file("source2.txt")
# переводим данные в формат словаря в графе
graph_1 = data_to_graph(raw_data_1)
# переводим данные в формат словаря в графе
graph_2 = data_to_graph(raw_data_2)
fig, ax = plt.subplots()

fig.set_size_inches(8, 6)

# TODO добавить проверку совпадений типов транзисторов
#print(networkx.vf2pp_is_isomorphic(graph_1, graph_2))
networkx.draw_random(graph_1, with_labels=True)
plt.show()
