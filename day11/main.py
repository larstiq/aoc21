#!/usr/bin/env python

import pandas as pd
import numpy as np
import time
from scipy.ndimage.measurements import label, morphology

flash_struc = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]], dtype=bool)

with open("tinput") as puzzle_input:
    data = [list(map(int, line.strip())) for line in puzzle_input]
    octopi = pd.DataFrame(data=data)

    flashes = 0
    for step in range(3):
        flashed = np.zeros_like(octopi, dtype=bool)
        charge = octopi + 1
        nines = charge > 9
        flashed = nines
        new_nines = nines
        print(charge)
        print(nines)

        print(flash_neighbours)

        while new_nines.any().any():
            flash_neighbours = pd.DataFrame(morphology.grey_dilation(new_nines, footprint=flash_struc, mode='constant', cval=-1))
            print("flashn", flash_neighbours)
            charge[flash_neighbours] = charge[flash_neighbours] + 1
            print(charge)
            new_nines = (charge > 9) & ~flashed
            print(new_nines)
            flashed = flashed | flash_neighbours
            print(flashed)

        charge[flashed] = 0
        octopi = charge
