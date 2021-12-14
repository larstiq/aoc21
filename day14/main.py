#!/usr/bin/env python3.10

#import pandas as pd
#import numpy as np
import itertools
from collections import Counter


pairs = {}
with open("simput") as puzzle_input:
    polymer = list(puzzle_input.readline().strip())
    puzzle_input.readline()
    for line in puzzle_input:
        left, right = line.strip().split(" -> ")
        pairs[tuple(left)] = right

    print(pairs)
    for step in range(10):
        new_polymer = []
        for pair in itertools.pairwise(polymer):
            extras.append(pairs[pair])

        print(f"{extras=}")
        print(f"{polymer=}")

        polymer = list(itertools.chain(*zip(polymer, extras)))
        print(f"{polymer=}")
        print(polymer)
        print(len(polymer))

    print(Counter(polymer))
    

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

    

