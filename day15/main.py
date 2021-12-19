#!/usr/bin/env python

import networkx as nx
import pandas as pd
import numpy as np
import time

directions = [
    (-1, 0), (1, 0), (0, -1), (0, 1)
]


def time_since(t, description=""):
    now = time.time()
    print(f"Time elapsed since previous timestamp {description}", now - t)
    return now

def show(cave):
    for ix, row in cave.iterrows():
        print("".join(map(str, row)))

with open("input") as puzzle_input:
    t0 = time.time()
    data = [list(map(int, line.strip())) for line in puzzle_input]
    df = pd.DataFrame(data)
    t1 = time_since(t0, "[Data read in]")

    
    G = nx.DiGraph()

    positions = df.stack().index
    G.add_nodes_from(positions)

    for pos in positions:
        for direct in directions:
            neighbour = pos[0] + direct[0], pos[1] + direct[1]
            if neighbour in positions:
                # edge wieght
                #G.add_edge(pos, neighbour, weight=df.loc[neighbour])
                G.add_edge(pos, neighbour)

    t2 = time_since(t1, "[Graph constructed]")

    def func(u, v, d):
        return df.loc[v]

    path = nx.algorithms.shortest_paths.dijkstra_path(G, (0, 0), positions[-1], func)
    print(sum(df.loc[pos] for pos in path[1:]))
    t3 = time_since(t2, "[Path on small graph found]")


    w, h = df.shape
    biggermap = pd.DataFrame(data=np.zeros(shape=(5 * w, 5 * h), dtype=int))
    for x in range(5):
        for y in range(5):

            pf = pd.DataFrame(index=df.index + x * w, columns=df.columns + y * h, data=df.values + x + y)
            pf[pf > 19] = pf[pf > 19] - 9
            pf[pf > 9] = pf[pf > 9] - 9
            biggermap[pf > 0] = pf

    t4 = time_since(t3, "[Big map constructed]")


    H = nx.DiGraph()

    big_positions = biggermap.stack().index
    H.add_nodes_from(big_positions)

    def big_func(u, v, d):
        return biggermap.loc[v]

    for pos in big_positions:
        for direct in directions:
            neighbour = pos[0] + direct[0], pos[1] + direct[1]
            if neighbour in big_positions:
                # edge wieght
                #G.add_edge(pos, neighbour, weight=df.loc[neighbour])
                H.add_edge(pos, neighbour)

    t5 = time_since(t4, "[Big graph constructed]")

    bigpath = nx.algorithms.shortest_paths.dijkstra_path(H, (0, 0), big_positions[-1], big_func)

    bigsum = sum(biggermap.loc[pos] for pos in bigpath[1:])
    print(bigsum)
    t6 = time_since(t5, "[Path on big graph found]")

    #print(G)
    #print(data)

