from dataclasses import dataclass

import itertools
import numpy as np
import networkx
import matplotlib.patches as patches
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def read_file(name):
    result = {}
    flag = 0
    with open(name, "r") as file:
        program_name = file.readline()
        while True:
            line_one = file.readline()
            if not line_one:
                break
            curr_line = line_one.split()
            if len(curr_line):
                if curr_line[0] == "L":
                    layer_name = curr_line[1].replace(";","")
                    line_two = file.readline().split()
                    if line_two[0] == "P":
                        if layer_name not in result.keys():
                            result[layer_name] = []
                        polygon = []
                        for i in range(1, len(line_two), 2):
                            polygon.append((int(line_two[i].replace(";", "")), int(line_two[i+1].replace(";", ""))))
                        result[layer_name].append(polygon)
                    if line_two[0] == "4N":
                        if layer_name not in result.keys():
                            result[layer_name] = []
                        result[layer_name].append([line_two[1], int(line_two[2]), int(line_two[3].replace(";",""))])
                        line_three = file.readline()
                if curr_line[0] == "DS":
                    continue
    return result

data = read_file("sum.cif")
print(data)
print(data.keys())

num_keys = len(data.keys())
colors = cm.viridis(np.linspace(0, 1, num_keys))

# Generate the dictionary
color_dict = {key: color for key, color in zip(data.keys(), colors)}
# Create a new figure and axis
fig, ax = plt.subplots()

for key in data.keys():
    print(key)
    if key in ["TSP", "TM1", "TM2", "TSN"]:
        continue
    for vertices in data[key]:
        polygon = patches.Polygon(vertices, closed=True, linewidth=1, edgecolor=color_dict[key], facecolor='none')
        ax.add_patch(polygon)


ax.set_xlim(-10000, 10000)
ax.set_ylim(-10000, 10000)

# Show the plot
plt.show()




