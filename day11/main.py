#!/usr/bin/env python

import pandas as pd
import numpy as np
import time
from scipy.ndimage.measurements import label, morphology

flash_struc = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]], dtype=bool)

directions = [
    (-1, -1), (-1, 0), (-1, 1),
    ( 0, -1),          ( 0, 1),
    ( 1, -1), ( 1, 0), ( 1, 1),
]


def show_octopi(greeting, friends):
    print(greeting)
    for row in friends.astype(int).iterrows():
        print("".join(map(str, row[1])))
    print()


with open("input") as puzzle_input:
    data = [list(map(int, line.strip())) for line in puzzle_input]
    octopi = pd.DataFrame(data=data)

    step = 0
    flashes = 0
    synchronized = False
    while not synchronized:
        step = step + 1
        flashed = np.zeros_like(octopi, dtype=bool)

        # All the octopi charge up their flashlights
        octopi = octopi + 1
        charged = octopi > 9

        while charged.any().any():
            df = charged.stack()
            for location in df[df].index:
                for direction in directions:
                    neighbour = location[0] + direction[0], location[1] + direction[1]

                    if (neighbour[0] >= 0 and neighbour[1] >= 0 and
                        neighbour[0] < octopi.shape[0] and
                        neighbour[1] < octopi.shape[1]):
                        octopi.loc[neighbour] = octopi.loc[neighbour] + 1

            flashed = flashed | charged
            charged = (octopi > 9) & ~flashed

        # After flashing the charge level starts at zero
        octopi[flashed] = 0

        flashes = flashes + flashed.sum().sum()

        if step == 100:
            print("Flashes", flashes)
        synchronized = flashed.all().all()
        if synchronized:
            print("Synchronized at step", step)
