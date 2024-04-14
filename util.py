# -*- coding: utf-8 -*-
from shapely.geometry import Polygon
from dataclasses import dataclass, make_dataclass, fields
from collections import defaultdict
#тут находится гайд по порядку слоев для детекта
#он существует чтобы убрать код КОТОРЫЙ НЕ ПОНРАВИЛСЯ АНЕ
#И ОНА НАЗВАЛА МЕНЯ ЯНДЕРЕ ДЕВОМ
#ЧТО Я НИКОГДА ЕЙ НЕ ПРОЩУ
guide = {
    "n_transistor" : ["SN", "NA"],
    "p_transistor" : ["SP", "NA", "P"],
    "r_contact" : ["CNA", "NA", "M1", "CNA", "NA", "M1", "M1"],
    "b_contact" : ["CPA", "NA", "M1", "P", "CPA", "NA", "M1", "P", "M1"],
    "m_contact" : ["P", "NA", "NA", "CNE", "M1", "M1"],
    "Eqwi_NA_PE_contact" : ["NA", "NA", "P", "CPE", "M1", "M1"],
    "CNA_dot_contact": ["CNA", "NA", "M1"],
    "CPA_dot_contact": ["CPA", "NA", "M1", "P"],
    "CSI_dot_contact": ["CSI", "SI", "M1"],
    "CM1_dot_contact": ["CM1", "M1", "M2"],
    "SI_rail" : ["SI"],
    "M1_rail" : ["M1"],
    "M2_rail" : ["M2"],
    #"b_pocket" : ["KN"],
}
classes = {}
def mark_duplicates(lst):
    counts = defaultdict(int)
    marked_list = []

    for item in lst:
        counts[item] += 1
        marked_list.append(item + (str(counts[item]) if counts[item] > 1 else ''))

    return marked_list

def create_dataclasses(class_dict):
    global classes
    for class_name, attributes in class_dict.items():
        # Define field names and types for the dataclass
        fields_dict = {name: Polygon for name in mark_duplicates(attributes)}

        # Create the dataclass with the specified fields
        DataClass = make_dataclass(class_name, fields_dict.items(), frozen=True, eq=False)

        # Store the generated dataclass
        classes[class_name] = DataClass

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


def read_general_component(file, data: dict, component_name, num_of_layers, number):
    polygons = []
    for i in range(num_of_layers):
        file.readline()
        layer_line = file.readline().split()
        polygon = convert_list_to_poly(layer_line[1:])
        polygons.append(polygon)
    contact = classes[component_name](*polygons)
    data[component_name + str(number)] = contact
    return contact

def transform_lines_to_component(file, data, number, component):
    read_general_component(file, data, component, len(guide[component]), number)


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
    global guide
    create_dataclasses(guide)
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

