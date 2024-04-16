# -*- coding: utf-8 -*-
import networkx
import networkx as nx

from dataclasses import dataclass
from .util import *
from .topology import n_transistor, p_transistor
import matplotlib.patches as patches
import matplotlib
import matplotlib.image as image
from dataclasses import asdict

matplotlib.use("TkAgg")
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from shapely.geometry import MultiPolygon


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
