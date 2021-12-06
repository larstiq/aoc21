#!/usr/bin/env python

import pandas as pd
import numpy as np

with open("input") as puzzle_input:
    fishes = pd.read_csv(puzzle_input, header=None).transpose()
    fish_generations = fishes.value_counts()

# Each time step fish in generation N move to generation N-1 except for
# generation 0 which split into 6 and 8.
#
# That's expressed by the following generation transition matrix:
transition = pd.DataFrame([
    (0, 1, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 1, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 1, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 1, 0, 0),
    (1, 0, 0, 0, 0, 0, 0, 1, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0),
])

# Convert the initial input of individual fishes into a generation count
fish_gen_vector = []
for ix in range(9):
    if ix in fish_generations:
        fish_gen_vector.append(fish_generations.loc[ix].sum())
    else:
        fish_gen_vector.append(0)
fish_gen_vector = pd.Series(fish_gen_vector)
print(fish_gen_vector)


# Visually confirm the result are correct, fishes should "swim left"
def simulate():
    fish_gen_vectors = [fish_gen_vector]
    for day in range(256):
        old = fish_gen_vectors[-1]
        fish_gen_vectors.append(transition.dot(old))
        new = fish_gen_vectors[-1]

        print(f"day {day}")
        print(old.values)
        print(new.values)
        print(new.sum())
    return fish_gen_vectors

# Actual math optimized solution is to take the `dayth` power of the transition
# matrix and apply that to the initial fish generation vector once.
def matrix_power():
    endtimes = np.linalg.matrix_power(transition, 256).dot(fish_gen_vector)
    print(endtimes)
    print(endtimes.sum().sum())

simulate()
matrix_power()
