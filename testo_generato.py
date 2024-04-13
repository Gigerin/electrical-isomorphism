import random

import networkx
import networkx as nx
import json
import os
def generate_connected_graph(num_vertices):
    # Generate a random connected graph
    while True:
        # Create a graph with the specified number of vertices
        G = nx.Graph()
        G.add_nodes_from(range(num_vertices))

        # Connect the graph randomly
        for i in range(num_vertices):
            if i > 0:
                # Connect each vertex to a randomly selected previous vertex
                prev_vertex = random.randint(0, i - 1)
                G.add_edge(i, prev_vertex)

        # Check if the graph is connected
        if nx.is_connected(G):
            break

    return G

def add_random_edges(G, num_edges_to_add):
    num_vertices = len(G)
    edges_to_add = set()

    # Generate random edges that are not already present in the graph
    while len(edges_to_add) < num_edges_to_add:
        u = random.randint(0, num_vertices - 1)
        v = random.randint(0, num_vertices - 1)
        if u != v and not G.has_edge(u, v):
            edges_to_add.add((u, v))

    # Add the random edges to the graph
    G.add_edges_from(edges_to_add)

def delete_random_edges(G, num_edges_to_delete):
    edges_to_delete = random.sample(G.edges(), num_edges_to_delete)
    G.remove_edges_from(edges_to_delete)

def morph_graph(graph):
    morphed = graph.copy()
    add_random_edges(morphed, 28)
    delete_random_edges(morphed, 28)
    return morphed
# Example usage:
num_vertices = 15  # Change this to the desired number of vertices
graph = generate_connected_graph(num_vertices)
morphed = morph_graph(graph)
print("Random connected graph with", num_vertices, "vertices:")
print("Edges:", graph.edges())
print("Random connected graph with", len(morphed.nodes), "vertices:")
print("Edges:", morphed.edges())
isomorphic = networkx.vf2pp_is_isomorphic(graph, morphed)
print(isomorphic)


def scramble(graph_in):
    G = graph_in.copy()
    nodes = list(G.nodes())

    # Randomly permute the nodes
    random.shuffle(nodes)

    # Create a mapping from original nodes to permuted nodes
    mapping = {old_node: new_node for old_node, new_node in zip(G.nodes(), nodes)}

    # Create a new graph with the permuted nodes but the same edges
    H = nx.relabel_nodes(G, mapping)

    print(networkx.vf2pp_is_isomorphic(graph, H))
    return H
def generate_test(truthfulness, graph):
    morphed = morph_graph(graph)
    isomorphic = networkx.vf2pp_is_isomorphic(graph, morphed)
    while isomorphic != truthfulness:
        morphed = scramble(graph)
        isomorphic = networkx.vf2pp_is_isomorphic(graph, morphed)
    return morphed

true_count = 0
false_count =10

while true_count < 20:
    graph = generate_connected_graph(num_vertices)
    folder = os.getcwd()+"\\tests\\true\\"+str(true_count)+"\\"
    os.mkdir(folder)
    file_name = "graph1.xml"
    nx.write_graphml(graph, folder+file_name)  # Save graph to file
    morphed = generate_test(True, graph)
    file_name = "graph2.xml"
    nx.write_graphml(morphed, folder+file_name)  # Save graph to file
    num_vertices += 1
    true_count += 1
"""
while false_count < 16:
    graph = generate_connected_graph(num_vertices)
    folder = os.getcwd()+"\\tests\\false\\"+str(false_count)+"\\"
    os.mkdir(folder)
    file_name = "graph1.xml"
    nx.write_graphml(graph, folder+file_name)  # Save graph to file
    morphed = generate_test(False, graph)
    file_name = "graph2.xml"
    nx.write_graphml(morphed, folder+file_name)  # Save graph to file
    num_vertices += 1
    false_count += 1


"""