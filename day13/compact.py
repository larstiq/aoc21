#!/usr/bin/env python

import networkx as nx


def walk(G, visit_max=1, visit_maxed=0, path=None):
    if path is None:
        path = ["start"]

    current = path[-1]
    paths = set()
    for neighbour in G[current]:
        if neighbour == "end":
            subpaths = {tuple(path + [neighbour])}
        elif neighbour == "start":
            subpaths = set()
        elif neighbour.upper() == neighbour and current != neighbour:
            subpaths = walk(G, visit_max, visit_maxed, path + [neighbour])
        elif neighbour.lower() == neighbour:
            if neighbour not in path:
                subpaths = walk(G, visit_max, max(visit_maxed, 1), path + [neighbour])
            elif visit_maxed < visit_max:
                subpaths = walk(G, visit_max, visit_maxed + 1, path + [neighbour])
            else:
                subpaths = set()
        else:
            subpaths = set()

        paths.update(subpaths)

    return paths


G = nx.read_edgelist("input", delimiter="-")
print(len(walk(G)))
print(len(walk(G, 2)))
