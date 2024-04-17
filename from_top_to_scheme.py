# -*- coding: utf-8 -*-
import networkx as nx
from dataclasses import dataclass
from util import read_file_to_list
from shapely.geometry import Polygon
import matplotlib.pyplot as plt


@dataclass(frozen=True, eq=False)
class NPN_trans:
    in_out: [Polygon, Polygon]
    zatvor: Polygon
    channel: Polygon


@dataclass(frozen=True, eq=False)
class PNP_trans:
    in_out: [Polygon, Polygon]
    zatvor: Polygon
    channel: Polygon


def create_n_trans(topological_transistor):
    NA_layer = topological_transistor.NA
    SN_layer = topological_transistor.SN
    in_out = list(NA_layer.difference(SN_layer).geoms)
    zatvor = SN_layer
    channel = SN_layer.intersection(NA_layer)
    trans = NPN_trans(in_out, zatvor, channel)
    return trans

def create_p_trans(topological_transistor):
    SP_layer = topological_transistor.SP
    NA_layer = topological_transistor.NA
    in_out = list(NA_layer.difference(SP_layer).geoms)
    zatvor = SP_layer
    channel = SP_layer.intersection(NA_layer)
    trans = NPN_trans(in_out, zatvor, channel)
    return trans


def convert_top_dict_to_elec_dict(data):
    for key in data.keys():
        if "n_transistor" in key:
            data[key] = create_n_trans(data[key])
        if "p_transistor" in key:
            data[key] = create_p_trans(data[key])


if __name__ == "__main__":
    file_name = input("Please enter name of file(blank for default):")
    if not file_name:
        file_name = "LOGIC2.txt"
    data = read_file_to_list(file_name)
    convert_top_dict_to_elec_dict(data)





