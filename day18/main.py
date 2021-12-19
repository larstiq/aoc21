#!/usr/bin/env python

import networkx as nx
import pandas as pd
import numpy as np
from math import ceil
from scipy.spatial import ConvexHull



class SnailfishNumber:

    def __init__(self, number):
        self.root = number


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
    right = list(topological_sort(nt2).right()

    nx.algorithms.tree.operations.join([nt1, nt2])




with open("simput") as puzzle_input:
    numbers = [eval(line.replace("[", "(").replace("]", ")")) for line in puzzle_input]
    #numbers = [eval(line) for line in puzzle_input]


    t = number_to_tree(numbers[0])
    t2 = number_to_tree(numbers[1])
