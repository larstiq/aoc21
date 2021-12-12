#!/usr/bin/env python

import pandas as pd
import numpy as np
import time
from scipy.ndimage.measurements import label, morphology
import networkx as nx
import matplotlib

with open("simput") as puzzle_input:
    #data = pd.read_csv(puzzle_input, sep=0, header=None)
    data = [line.strip().split("-") for line in puzzle_input]

    G = nx.from_edgelist(data, create_using=nx.MultiGraph)

    #for node in G.nodes:
    #    if node.upper() == node:
    #        G.add_edge(node, node)

    simple_paths = list(nx.all_simple_paths(G, source='start', target='end'))


nx.draw(G)
nx.draw(nx.bfs_tree(G, 'start'))
visited_small = set()
current = 'start'
paths = {}

print(G[current])

for neighbour in G[current]:
    if neighbour.lower() == neighbour and neighbour not in visited_small:
        path_so_far.extend(neighbour)
        

def rec_visit(G, path, visited):
    current = path[-1]
    paths = []
    for neighbour in G[current]:
        if neighbour == 'end':
            subpaths = [path + [neighbour]]
        elif neighbour not in visited:
            subpaths = rec_visit(G, path + [neighbour], visited | {neighbour})
        elif neighbour.upper() == neighbour and current != neighbour:
            # TODO: cycles?
            subpaths = rec_visit(G, path + [neighbour], visited)

        paths.extend(subpath)

    return paths


    



list(nx.all_simple_paths(G, source='A', target='A'))

len(simple_paths)

H = G.copy()
for node in G:
    if node.upper() == node:
        for neighbour in G[node]:
            if neighbour.lower() == neighbour:
                for other in G[node]:
                    if other != neighbour and other.lower() == other:
                        replace_node = f"{neighbour}-replace-{node}-{other}"
                        H.add_node(replace_node)
                        H.add_edge(neighbour, replace_node)
                        H.add_edge(replace_node, other)

nx.draw_networkx(H)

nx.draw_networkx(nx.path_graph(G))

help(nx.path_graph)

list(nx.all_simple_paths(H, source='start', target='end'))

simple_paths
