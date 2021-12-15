#!/usr/bin/env python

import networkx as nx
import pandas as pd
import numpy as np

directions = [
    (-1, 0), (1, 0), (0, -1), (0, 1)
]

def show(cave):
    for ix, row in cave.iterrows():
        print("".join(map(str, row)))

with open("input") as puzzle_input:
    data = [list(map(int, line.strip())) for line in puzzle_input]
    df = pd.DataFrame(data)

    
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

    def func(u, v, d):
        return df.loc[v]

    path = nx.algorithms.shortest_paths.dijkstra_path(G, (0, 0), positions[-1], func)
    print(sum(df.loc[pos] for pos in path[1:]))


    w, h = df.shape
    biggermap = pd.DataFrame(data=np.zeros(shape=(5 * w, 5 * h), dtype=int))
    for x in range(5):
        for y in range(5):

            pf = pd.DataFrame(index=df.index + x * w, columns=df.columns + y * h, data=df.values + x + y)
            pf[pf > 19] = pf[pf > 19] - 9
            pf[pf > 9] = pf[pf > 9] - 9
            biggermap[pf > 0] = pf


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


    bigpath = nx.algorithms.shortest_paths.dijkstra_path(H, (0, 0), big_positions[-1], big_func)

    bigsum = sum(biggermap.loc[pos] for pos in bigpath[1:])
    print(bigsum)

    #print(G)
    #print(data)

