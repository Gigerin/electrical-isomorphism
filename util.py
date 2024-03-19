# -*- coding: utf-8 -*-
from shapely.geometry import Polygon
from dataclasses import dataclass

#тут находится гайд по порядку слоев для детекта
#он существует чтобы убрать код КОТОРЫЙ НЕ ПОНРАВИЛСЯ АНЕ
#И ОНА НАЗВАЛА МЕНЯ ЯНДЕРЕ ДЕВОМ
#ЧТО Я НИКОГДА ЕЙ НЕ ПРОЩУ
guide = {
    "n_transistor" : ["SN", "NA"],
    "p_transistor" : ["SP", "NA", "P"],
    "r_contact" : ["CNA", "NA", "M1", "CNA", "NA", "M1", "M1"],
    "b_contact" : ["CPA", "NA", "M1", "P", "CPA", "NA", "M1", "P", "M1"],
    "m_contact" : ["P", "NA", "NA", "CNE", "M1", "M1"]
}
@dataclass(frozen=True, eq=False)
class n_transistor:
    SN_layer: Polygon
    NA_layer: Polygon


@dataclass(frozen=True, eq=False)
class p_transistor:
    SP_layer: Polygon
    P_layer: Polygon
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

@dataclass(frozen=True, eq=False)
class m_contact:
    P_layer: Polygon
    NA_layer: Polygon
    NA_layer2: Polygon
    CNE_layer: Polygon
    M1_layer: Polygon
    M1_layer2: Polygon

def convert_list_to_poly(list):
    """
    Конвертируем список точек формата cif в формат многоугольников
    :param list:
    :return:
    """
    polygon = []
    for i in range(0, len(list), 2):
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
    polygons = []
    for i in range(2):
        file.readline()
        layer_line = file.readline().split()
        polygon = convert_list_to_poly(layer_line[1:])
        polygons.append(polygon)
    transistor = n_transistor(*polygons)
    data["n_transistor" + str(number)] = transistor
    return transistor


def read_p_transistor(file, data: dict, number):
    """
    программа добавления строк на случай p транзистора
    :param file:
    :param data:
    :param number:
    :param extra_line:
    :return:
    """
    polygons = []
    for i in range(3):
        file.readline()
        layer_line = file.readline().split()
        polygon = convert_list_to_poly(layer_line[1:])
        polygons.append(polygon)
    transistor = p_transistor(*polygons)
    data["p_transistor" + str(number)] = transistor
    return transistor

def read_r_contact(file, data, number):
    polygons = []
    for i in range(7):
        file.readline()
        layer_line = file.readline().split()
        polygon = convert_list_to_poly(layer_line[1:])
        polygons.append(polygon)
    contact = r_contact(*polygons)
    data["r_contact" + str(number)] = contact
    return contact

def read_b_contact(file, data, number):
    polygons = []
    for i in range(9):
        file.readline()
        layer_line = file.readline().split()
        polygon = convert_list_to_poly(layer_line[1:])
        polygons.append(polygon)
    contact = b_contact(*polygons)
    data["b_contact" + str(number)] = contact
    return contact

def read_m_contact(file, data, number):
    polygons = []
    for i in range(6):
        file.readline()
        layer_line = file.readline().split()
        polygon = convert_list_to_poly(layer_line[1:])
        polygons.append(polygon)
    contact = m_contact(*polygons)
    data["m_contact" + str(number)] = contact
    return contact


def transform_lines_to_component(file, data, number, component):
    if component == "r_contact":
        read_r_contact(file, data, number)
    if component == "b_contact":
        read_b_contact(file, data, number)
    if component == "m_contact":
        read_m_contact(file, data,number)
    if component == "n_transistor":
        read_n_transistor(file, data, number)
    if component == "p_transistor":
        read_p_transistor(file, data, number)


def match_layer_name_to_component(layers: list):
    global guide
    targets = guide.keys()  #можно удалять цель если не совпало а не проверять весь спиоск
    for i in range(len(layers)):
        for target in targets:
            if layers[:i] == guide[target]:
                return target
    return None

def get_line(file):
    return file.readline().replace(";", "").split()
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
    layer_names = []
    layer_polys = []
    with open("source/" + name, "r") as f:
        while True:
            line = f.readline().split()
            if line:
                if line[0] == "DS":
                    f.readline()
                    break
        while True:
            last_pos = f.tell()  # Запоминаем позицию на случай если не найдем никакого соответствия
            layer_name = f.readline().replace(";", "").split()
            if not layer_name:
                continue
            layer_poly = f.readline().replace(";", "").split()
            if layer_name[0] == "DF" or layer_poly[0] == "DF":
                break
            f.seek(last_pos)
            for i in range(9):
                layer_names = layer_names + get_line(f)[-1:]
                layer_polys.append(get_line(f))
            component = match_layer_name_to_component(layer_names)
            if component:
                f.seek(last_pos)
                transform_lines_to_component(f, result, number, component)

            else:
                f.seek(last_pos)
                garbage_list.append([f.readline().split(), f.readline().split()])
            number += 1
            layer_names = []
            layer_polys = []
    return result
