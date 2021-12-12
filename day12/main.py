#!/usr/bin/env python

import pandas as pd
import numpy as np
import time
from scipy.ndimage.measurements import label, morphology
import networkx as nx
import matplotlib

def to_graph(text):
    data = [line.strip().split("-") for line in text]
    G = nx.from_edgelist(data, create_using=nx.MultiGraph)
    return G

def rec_visit(G, path, max_small_visit=1, max_small_visited=0):
    current = path[-1]
    paths = []
    for neighbour in G[current]:
        if neighbour == 'end':
            subpaths = [path + [neighbour]]
        elif neighbour == 'start':
            subpaths = []
        elif neighbour.upper() == neighbour and current != neighbour:
            # TODO: cycles?
            subpaths = rec_visit(G, path + [neighbour], max_small_visit, max_small_visited)
        elif neighbour.lower() == neighbour:
            if neighbour not in path:
                subpaths = rec_visit(G, path + [neighbour], max_small_visit, max_small_visited)
            elif max_small_visited < max_small_visit:
                subpaths = rec_visit(G, path + [neighbour], max_small_visit, max_small_visited + 1)
            else:
                subpaths = []
        else:
            subpaths = []

        paths.extend(subpaths)

    return paths


smallin = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
small_graph = to_graph(smallin.split("\n"))

smallout = """start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,end
start,A,c,A,b,A,end
start,A,c,A,b,end
start,A,c,A,end
start,A,end
start,b,A,c,A,end
start,b,A,end
start,b,end"""

smallout_paths = [line.strip().split(",") for line in smallout.split("\n")] 
#assert set(tuple(l) for l in rec_visit(small_graph, ['start'])) == set(tuple(l) for l in smallout_paths)



midin = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""


mid_graph = to_graph(midin.split("\n"))
midout  = """start,HN,dc,HN,end
start,HN,dc,HN,kj,HN,end
start,HN,dc,end
start,HN,dc,kj,HN,end
start,HN,end
start,HN,kj,HN,dc,HN,end
start,HN,kj,HN,dc,end
start,HN,kj,HN,end
start,HN,kj,dc,HN,end
start,HN,kj,dc,end
start,dc,HN,end
start,dc,HN,kj,HN,end
start,dc,end
start,dc,kj,HN,end
start,kj,HN,dc,HN,end
start,kj,HN,dc,end
start,kj,HN,end
start,kj,dc,HN,end
start,kj,dc,end"""

mid_paths = [line.strip().split(",") for line in midout.split("\n")]

#assert set(tuple(l) for l in rec_visit(mid_graph, ['start'], {'start'})) == set(tuple(l) for l in mid_paths)


bigin = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""
big_graph = to_graph(bigin.split("\n"))
big_result = rec_visit(big_graph, ['start'])


with open("input") as puzzle_input:
    #data = pd.read_csv(puzzle_input, sep=0, header=None)
    G = to_graph([line for line in puzzle_input])
    aa = rec_visit(G, ['start'])
    print(len(aa))
    bb = rec_visit(G, ['start'], 2)
    print(len(bb))

    #assert set(tuple(l) for l in aa) == set(tuple(l) for l in smallout_paths)
