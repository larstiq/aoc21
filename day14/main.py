#!/usr/bin/env python3.10

#import pandas as pd
#import numpy as np
import itertools
from collections import Counter


pairs = {}
with open("input") as puzzle_input:
    polymer = list(puzzle_input.readline().strip())
    puzzle_input.readline()
    for line in puzzle_input:
        left, right = line.strip().split(" -> ")
        pairs[tuple(left)] = right

    print(pairs)
    for step in range(10):
        new_polymer = []
        for ix, char in enumerate(polymer):
            new_polymer.append(char)
            try:
                new_polymer.append(pairs[(char, polymer[ix + 1])])
            except:
                pass

        polymer = new_polymer
        print(len(polymer))

    count = Counter(polymer)
    print(count)
    print(count.most_common()[0][1] - count.most_common()[-1][1])

    

def with_counter():
    polymer_count = Counter()

    for pair in itertools.pairwise(polymer):
        polymer_count[pair] += 1

    print(polymer_count)

    for step in range(10):
        new_polymer = Counter()
        for pair in polymer_count:
            new_polymer[(pair[0], pairs[pair])] += 1
            new_polymer[(pairs[pair], pair[1])] += 1

        polymer_count = new_polymer

    print(polymer_count)

    

