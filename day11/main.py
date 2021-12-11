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

with open("tinput") as puzzle_input:
    data = [list(map(int, line.strip())) for line in puzzle_input]
    octopi = pd.DataFrame(data=data)

    flashes = 0
    for step in range(3):
        flashed = np.zeros_like(octopi, dtype=bool)
        octopi = octopi + 1
        nines = octopi > 9
        flashed = nines
        new_nines = nines
        print(octopi)
        print(nines)

        while new_nines.any().any():
            for location in new_nines.stack()[new_nines.stack()].index:
                for direction in directions:
                    neighbour = location[0] + direction[0], location[1] + direction[1]

                    #breakpoint()
                    octopi.loc[neighbour] = octopi.loc[neighbour] + 1
                    #flash_neighbours = pd.DataFrame(morphology.grey_dilation(new_nines, footprint=flash_struc, mode='constant', cval=-1))
                    #print("flashn", flash_neighbours)
                    #breakpoint()
            flashed = flashed | new_nines
            new_nines = (octopi > 9) & ~flashed
            print(new_nines)
            print(flashed)
            print(octopi)

        octopi[flashed] = 0
        print("End of step", step)
        print(octopi)
        print('-' * 80)
