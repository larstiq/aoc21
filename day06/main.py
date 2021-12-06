#!/usr/bin/env python

import pandas as pd
import numpy as np

segments = []
with open("input") as puzzle_input:
    fishes = pd.read_csv(puzzle_input, header=None).transpose()
    fish_generations = fishes.value_counts()

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


fish_gen_vector = []
for ix in range(9):
    if ix in fish_generations:
        fish_gen_vector.append(fish_generations.loc[ix].sum())
    else:
        fish_gen_vector.append(0)
fish_gen_vector = pd.Series(fish_gen_vector)
print(fish_gen_vector)


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

def matrix_power():

    P = transition
    for day in range(255):
        P = P.dot(transition)

    print(P.dot(fish_gen_vector).sum().sum())


simulate()
matrix_power()
