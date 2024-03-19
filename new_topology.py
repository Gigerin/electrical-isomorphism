import numpy as np
import networkx
import matplotlib.patches as patches
import matplotlib
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as image
from util import *

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from shapely.geometry import Polygon
import time

TRANSISTOR_FILE_NAME = "static/png-clipart-transistor-npn-electronics-electronic-symbol-symbol-miscellaneous-electronics.png"






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



file_name = input("Please enter name of file(blank for default):")
if not file_name:
    file_name = "sum.cif"
data = read_file_to_list(file_name)
print(data)
print(data.keys())
