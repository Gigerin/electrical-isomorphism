# -*- coding: utf-8 -*-
import networkx as nx
from dataclasses import dataclass
from topology import n_transistor, p_transistor

from shapely.geometry import Polygon


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


def create_n_trans(topological_transistor: n_transistor):
    NA_layer = topological_transistor.NA_layer
    SN_layer = topological_transistor.SN_layer
    in_out = [NA_layer.difference(SN_layer), NA_layer.difference(SN_layer)]
    zatvor = SN_layer
    channel = SN_layer.intersection(NA_layer)
    trans = NPN_trans(in_out, zatvor, channel)
    return trans

def create_p_trans(topological_transistor: p_transistor):
    SP_layer = topological_transistor.SP_layer
    NA_layer = topological_transistor.NA_layer
    in_out = [NA_layer.difference(SP_layer), NA_layer.difference(SP_layer)]
    zatvor = SP_layer
    channel = SP_layer.intersection(NA_layer)
    trans = NPN_trans(in_out, zatvor, channel)
    return trans

