#!/usr/bin/env python

import networkx as nx


def walk(G, visitation_limit=1, visited_max=0, path=None):
    if path is None:
        path = ["start"]

    current = path[-1]
    paths = set()
    for next_cave in G[current]:
        if next_cave == "end":
            subpaths = {tuple(path + [next_cave])}
        elif next_cave == "start":
            subpaths = set()

        # Big caves have no visitation limit
        elif next_cave.upper() == next_cave:
            subpaths = walk(G, visitation_limit, visited_max, path + [next_cave])
        elif next_cave.lower() == next_cave:
            if next_cave not in path:
                # If no small cave has been visited yet, the max goes up to 1.
                # Otherwise pass on whatever is the maximum
                subpaths = walk(
                    G, visitation_limit, max(visited_max, 1), path + [next_cave]
                )
            elif visited_max < visitation_limit:
                # Small caves have not been visited as often as possible, up
                # the limit by one.  (Here is a bug btw if we need individual
                # tracking beyond 2)
                subpaths = walk(
                    G, visitation_limit, visited_max + 1, path + [next_cave]
                )
            else:
                subpaths = set()
        else:
            subpaths = set()

        paths.update(subpaths)

    return paths


def read_paths(filename):
    with open(filename) as finput:
        return {tuple(line.strip().split(",")) for line in finput}


small_graph = nx.read_edgelist("small_input", delimiter="-")
mid_graph = nx.read_edgelist("mid_input", delimiter="-")
large_graph = nx.read_edgelist("large_input", delimiter="-")


assert read_paths("small_output") == walk(small_graph)
assert read_paths("mid_output") == walk(mid_graph)
assert 226 == len(walk(large_graph))

assert read_paths("small_output2") == walk(small_graph, 2)
assert 103 == len(walk(mid_graph, 2))
assert 3509 == len(walk(large_graph, 2))


G = nx.read_edgelist("input", delimiter="-")

assert 3000 == len(walk(G))
assert 74222 == len(walk(G, 2))
