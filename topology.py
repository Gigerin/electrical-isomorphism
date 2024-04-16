import numpy as np
import networkx
import matplotlib.patches as patches
import matplotlib
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as image
from dataclasses import dataclass

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from shapely.geometry import Polygon
import time

TRANSISTOR_FILE_NAME = "static/png-clipart-transistor-npn-electronics-electronic-symbol-symbol-miscellaneous-electronics.png"

"""
BAD FILE DO NOT USE 
NOT FOR PRODUCTION
"""
@dataclass(frozen=True, eq=False)
class n_transistor:
    SN_layer: Polygon
    NA_layer: Polygon


@dataclass(frozen=True, eq=False)
class p_transistor:
    P_layer: Polygon
    SP_layer: Polygon
    NA_layer: Polygon

@dataclass(frozen=True, eq=False)
class b_contact:
    CPA_layer: Polygon
    NA_layer: Polygon
    M1_layer: Polygon
    P_layer: Polygon
    CPA_layer2: Polygon
    NA_layer2: Polygon
    M1_layer2: Polygon
    P_layer2: Polygon
    M1_layer3: Polygon

@dataclass(frozen=True, eq=False)
class r_contact:
    CNA_layer: Polygon
    NA_layer: Polygon
    M1_layer: Polygon
    CNA_layer2: Polygon
    NA_layer2: Polygon
    M1_layer2: Polygon
    M1_layer3: Polygon

def convert_list_to_poly(list):
    """
    Конвертируем список точек формата cif в формат многоугольников
    :param list:
    :return:
    """
    polygon = []
    for i in range(1, len(list) - 1, 2):
        polygon.append(
            (
                int(list[i].replace(";", "")),
                int(list[i + 1].replace(";", "")),
            )
        )
    return Polygon(polygon)


def read_n_transistor(file, data: dict, number):
    """
    программа добавления строк в качестве n транзистора
    :param file:
    :param data:
    :param number:
    :return:
    """
    second_line = file.readline().split()
    third_line = file.readline().split()
    fourth_line = file.readline().split()
    sp_poly = convert_list_to_poly(second_line[1:])
    na_poly = convert_list_to_poly(fourth_line[1:])
    transistor = n_transistor(sp_poly, na_poly)
    data["n_transistor" + str(number)] = transistor
    return transistor


def read_p_transistor(file, data: dict, number, *extra_line):
    """
    программа добавления строк на случай p транзистора
    :param file:
    :param data:
    :param number:
    :param extra_line:
    :return:
    """
    sn_layer = file.readline().split()
    na = file.readline().split()
    na_layer = file.readline().split()
    p_poly = convert_list_to_poly(extra_line[0][1:])
    sn_poly = convert_list_to_poly(sn_layer[1:])
    na_poly = convert_list_to_poly(na_layer[1:])
    transistor = p_transistor(p_poly, sn_poly, na_poly)
    data["p_transistor" + str(number)] = transistor

def read_r_contact(file, data, number):
    polygons = []
    for i in range(6):
        polygons.append(file.readline().strip())
        file.readline()
    polygons.append(file.readline().strip())
    contact = r_contact(*polygons)
    data["r_contact" + str(number)] = contact

def read_b_contact(file, data, number):
    polygons = []
    for i in range(8):
        polygons.append(file.readline().strip())
        file.readline()
    polygons.append(file.readline().strip())
    contact = b_contact(*polygons)
    data["b_contact" + str(number)] = contact


def read_file_to_list(name):
    """
    Основная функция отвечающая за парсинг файла и его обработку в формат полигонов
    Берется строка. Если она начинается на какую-то из комбинаций, которые описаны в readme.md
    то она обрабатывается как отдельный элемент схемы типа транзистора. Иначе, строка добавляется
    в garbage_list(временное решение проблемы. в идеале этот список мусора будет пуст)
    :param name:
    :return:
    """
    number = 1
    result = {}
    garbage_list = []
    with open("source/" + name, "r") as f:
        while True:
            line = f.readline().split()
            if line:
                if line[0] == "DS":
                    f.readline()
                    break
        while True:
            first_line = f.readline().split()
            if first_line[0] == "DF;":
                break
            if first_line[0] == "L":
                if first_line[1] == "SN;":
                    read_n_transistor(f, result, number)
                if first_line[1] == "SP;":
                    last_pos = f.tell()
                    second_line = f.readline().split()
                    third_line = f.readline().split()
                    fourth_line = f.readline().split()
                    if third_line[1] == "NA;":
                        f.readline().split()
                        read_p_transistor(f, result, number, second_line)
                        continue
                    else:
                        f.seek(last_pos)
                        print("I SHIT ")
                        garbage_list.append(
                            [first_line, second_line, third_line, fourth_line]
                        )
                if first_line[1] == "CNA;":
                    read_r_contact(f, result, number)
                    continue
                if first_line[1] == "CPA;":
                    read_b_contact(f, result, number)
                    continue

            second_line = f.readline().split()
            garbage_list.append([first_line, second_line])

            number += 1
    print(garbage_list)
    print(len(garbage_list))
    return result




def read_file(name):
    result = {}
    number = 0
    with open("source/" + name, "r") as file:
        program_name = file.readline()
        while True:
            line_one = file.readline()
            if not line_one:
                break
            curr_line = line_one.split()
            if len(curr_line):
                if curr_line[0] == "L":
                    layer_name = str(curr_line[1].replace(";", "")) + str(number)
                    line_two = file.readline().split()
                    if line_two[0] == "P":
                        if layer_name not in result.keys():
                            result[layer_name] = []
                        polygon = []
                        for i in range(1, len(line_two), 2):
                            polygon.append(
                                (
                                    int(line_two[i].replace(";", "")),
                                    int(line_two[i + 1].replace(";", "")),
                                )
                            )
                        if len(polygon) % 2 != 0:
                            polygon.insert(
                                len(polygon),
                                (polygon[len(polygon) - 1][0], polygon[0][1]),
                            )
                        result[layer_name] = Polygon(polygon)
                    if line_two[0] == "4N":
                        if layer_name not in result.keys():
                            result[layer_name] = []
                        result[layer_name] = [
                            line_two[1],
                            int(line_two[2]),
                            int(line_two[3].replace(";", "")),
                        ]
                        line_three = file.readline()
                if curr_line[0] == "DS" and curr_line[1] == "100":
                    break
            number = number + 1
    return result


def get_connections(initial_polygon: Polygon, polygon_layer: str, data: dict):
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


# showing the layers in matplotlib
transistor_img = image.imread(TRANSISTOR_FILE_NAME)


def show_circuit(data, transistors):
    num_keys = 10000
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    colors = cm.viridis(np.linspace(0, 1, num_keys))
    color_dict = {key: color for key, color in zip(data.keys(), colors)}
    for key in transistors:
        for prefix in ["TSP", "TM1", "TM2", "TSN"]:
            if key.startswith(prefix):
                xycoords = (transistors[key][1], transistors[key][2])
                imagebox = OffsetImage(transistor_img, zoom=0.01)
                ab = AnnotationBbox(imagebox, xycoords, frameon=False)
                ax.add_artist(ab)
    for key in data.keys():
        vertices = data[key]
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


def convert_data_to_graph(data):
    """
    Переводит словарь многоугольников в граф.
    :param data: входной словарь
    :return: граф
    """
    graph = networkx.Graph()
    sorted_polygons = sorted(data.keys(), key=lambda polygon: data[polygon].area)
    print(sorted_polygons)
    for key in sorted_polygons:
        polygon = data[key]
        if str(key)[0] == "C":
            connections = get_connections(polygon, key, data)
            graph.add_edge(connections[0], connections[1])
            continue
        if str(key)[0] == "P":
            connections = get_connections(polygon, key, data)
            pass
    for key in data.keys():
        if data[key] not in graph.nodes:
            graph.add_node(key, layer=polygon)
    return graph

"""
file_name = input("Please enter name of file(blank for default):")
if not file_name:
    file_name = "sum.cif"
data = read_file_to_list(file_name)
print(data)
print(data.keys())


transistors = {
    k: data.pop(k)
    for k in list(data.keys())
    if any(k.startswith(prefix) for prefix in ["TSP", "TM1", "TM2", "TSN", "CW", "M2A"])
}

graph = convert_data_to_graph(data)

graph_2 = graph.copy()

print(len(data.keys()))
start = time.time()
print(networkx.vf2pp_is_isomorphic(graph, graph_2))
end = time.time()

print(end - start)

print(len(data.keys()))

promezh = {}

keys = data.keys()
for key in keys:
    layer_name = ""
    for letter in key:
        if "0"<letter<"9":
            break
        else:
            layer_name += letter
    if layer_name in promezh:
        promezh[layer_name] += 1
    else:
        promezh[layer_name] = 1
print(promezh)

networkx.draw(graph, with_labels = True)
plt.show()

show_circuit(data, transistors)
"""
