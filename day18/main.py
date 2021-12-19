#!/usr/bin/env python

import networkx as nx
import pandas as pd
import numpy as np
from math import ceil
from scipy.spatial import ConvexHull


def sfn(number):
    return number_to_tree(eval(number.replace("[", "(").replace("]", ")")))

def number_to_tree(number, tree=None):

    if isinstance(number, int):
        return

    if tree is None:
        tree = nx.DiGraph()

    left, right = number[0], number[1]
    tree.add_node(number)
    tree.add_edge(number, left)
    tree.add_edge(number, right)
    number_to_tree(left)
    number_to_tree(right)

    return tree
    
    
def add(nt1, nt2):

    tree = nx.DiGraph()
    left = list(nx.topological_sort(nt1))[0]
    right = list(nx.topological_sort(nt2))[0]

    # just reconstruct from the roots
    number = (left, right)
    return number_to_tree(number)

def explode(tree):

    # find pair to explode

    root = list(nx.topological_sort(tree))[0]
    
    depth = 0
    left_nr = None
    right_nr = None
    explode_start = None
    explode_end = None
    for ix, char in enumerate(str(root)):
        if char == "(":
            depth += 1
        elif char == ")":
            if explode_start is not None:
                explode_end = ix
            depth -= 1
        elif char in "0123456789":
            if left_nr is None:
                left_nr = ix
            if explode_end is not None and right_nr is None:
                right_nr = ix

        if depth == 5 and explode_start is None:
            explode_start = ix

            print("Found pair to explode at", ix)






with open("simput") as puzzle_input:
    #numbers = [eval(line.replace("[", "(").replace("]", ")")) for line in puzzle_input]
    numbers = [line for line in puzzle_input]


    t1 = sfn(numbers[0])
    t2 = sfn(numbers[1])
    print(add(t1, t2))
