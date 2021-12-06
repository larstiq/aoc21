#!/usr/bin/env python

import pandas as pd
import numpy as np
import time

with open("input") as puzzle_input:
    fishes = pd.read_csv(puzzle_input, header=None).transpose()

# Each time step fish in generation N move to generation N-1 except for
# generation 0 which split into 6 and 8.
#
# That's expressed by the following generation transition matrix:
transition = pd.DataFrame(
    [
        (0, 1, 0, 0, 0, 0, 0, 0, 0),
        (0, 0, 1, 0, 0, 0, 0, 0, 0),
        (0, 0, 0, 1, 0, 0, 0, 0, 0),
        (0, 0, 0, 0, 1, 0, 0, 0, 0),
        (0, 0, 0, 0, 0, 1, 0, 0, 0),
        (0, 0, 0, 0, 0, 0, 1, 0, 0),
        (1, 0, 0, 0, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 1),
        (1, 0, 0, 0, 0, 0, 0, 0, 0),
    ]
)

# Or more compactly with numpy
T = np.roll(np.identity(9, dtype=int), -1, axis=0)
T[6, 0] = 1
assert pd.DataFrame(T).equals(transition)

# Convert the initial input of individual fishes into a generation count
# Since .value_counts() gives a multi-index and not every generation might be
# represented, do a .get(generation 0) to default
fish_generations = pd.Series(
    fishes.value_counts().get(generation, 0) for generation in range(9)
)


# Visually confirm the result are correct, fishes should "swim left"
def simulate(days):
    new = fish_generations
    simulated = [new]
    for day in range(days):
        new, old = transition.dot(new), new
        simulated.append(new)

        print(f"day {day}")
        print(old.values)
        print(new.values)
        print(new.sum())
    return simulated


# Actual math optimized solution is to take the `dayth` power of the transition
# matrix and apply that to the initial fish generation vector once.
def matrix_power():
    P = np.linalg.matrix_power(transition, 256)
    endtimes = P.dot(fish_generations)
    print(endtimes)
    print(endtimes.sum())
    return P, endtimes


# simulate()
matrix_power()
