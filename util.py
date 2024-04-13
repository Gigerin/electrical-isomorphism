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
    "b_contact" : ["CPA", "NA", "M1", "P", "CPA", "NA", "M1", "P"],
    "m_contact" : ["P", "NA", "NA", "CNE", "M1", "M1"],
    "g_contact" : ["SI"],
    "y_contact" : ["M1"],
    "с_contact" : ["M2"],
    #"b_pocket" : ["KN"],
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

@dataclass(frozen=True, eq=False)
class g_contact:
    SI_layer: Polygon
    #SI_layer2: Polygon

@dataclass(frozen=True, eq=False)
class y_contact:
    M1_layer: Polygon
    #M1_layer2: Polygon

@dataclass(frozen=True, eq=False)
class с_contact:
    M2_layer: Polygon
    #M1_layer2: Polygon

@dataclass(frozen=True, eq=False)
class b_pocket:
    KN_layer: Polygon
def convert_list_to_poly(list):
    """
    Конвертируем список точек формата cif в формат многоугольников
    :param list:
    :return:
    """
    polygon = []
    print(list)
    for i in range(0, len(list), 2):
        polygon.append(
            (
                int(list[i].replace(";", "")),
                int(list[i + 1].replace(";", "")),
            )
        )
    return Polygon(polygon)


def read_general_component(file, data: dict, component_name, num_of_layers, number):
    polygons = []
    for i in range(num_of_layers):
        file.readline()
        layer_line = file.readline().split()
        polygon = convert_list_to_poly(layer_line[1:])
        polygons.append(polygon)
    contact = eval(component_name)(*polygons)
    data[component_name + str(number)] = contact
    return contact

def transform_lines_to_component(file, data, number, component):
    operation = {
        "r_contact" : 7,
        "b_contact" : 9,
        "m_contact" : 6,
        "n_transistor" : 2,
        "p_transistor" : 3,
        "g_contact" : 1,
        "y_contact" : 1,
        "с_contact" : 1,
        "b_pocket" : 1
    }
    print(component)
    read_general_component(file, data, component, operation[component], number)


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
    print(len(garbage_list))
    with open("garbage.txt", "w") as f:
        for line in garbage_list:
            f.write((str(line)))
            f.write("\n")
    print(garbage_list)
    print(len(result))
    return result

