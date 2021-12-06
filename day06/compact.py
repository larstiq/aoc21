import pandas as pd
import numpy as np

with open("input") as puzzle_input:
    fishes = pd.read_csv(puzzle_input, header=None).transpose()

fish_generations = pd.Series(
    fishes.value_counts().get(generation, 0) for generation in range(9)
)

T = np.roll(np.identity(9, dtype=int), -1, axis=0)
T[6, 0] = 1
P = np.linalg.matrix_power(T, 256)
print(P.dot(fish_generations).sum())
