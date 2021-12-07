#!/usr/bin/env python

import pandas as pd
import numpy as np
import time

with open("input") as puzzle_input:
    crabs = pd.read_csv(puzzle_input, header=None).loc[0]

# Can't be worse
possible_positions = np.linspace(crabs.min(), crabs.max(), crabs.max() - crabs.min() + 1)

# TODO: crab gens
vc = crabs.value_counts(sort=False)
crab_positions = pd.Series(data=vc.index, index=vc.values)


def part1():
    fuel_costs = pd.DataFrame(columns=possible_positions, index=crab_positions)

    for pos in possible_positions:
        fuel_costs[pos] = abs(crab_positions.values - pos)

    all_costs = fuel_costs.T.dot(vc)
    print(all_costs.min(), all_costs.argmin())

def part2():
    fuel_costs = pd.DataFrame(columns=possible_positions, index=crab_positions)
    for pos in possible_positions:
        diff = abs(crab_positions.values - pos)
        fuel_costs[pos] = diff * (diff + 1)/2

    all_costs = fuel_costs.T.dot(vc)
    print(all_costs.min(), all_costs.argmin())


part2()
