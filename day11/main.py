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
    for row in pd.DataFrame(friends.astype(int)).iterrows():
        print("".join(map(str, row[1])))
    print()


with open("simput") as puzzle_input:
    data = [list(map(int, line.strip())) for line in puzzle_input]
    octopi = pd.DataFrame(data=data)

    debug = False
    flashes = 0
    for step in range(1, 4):
        flashed = np.zeros_like(octopi, dtype=bool)
        octopi = octopi + 1
        new_nines = octopi > 9
        show_octopi("after charge", octopi)
        show_octopi("new_nines", new_nines)

        while new_nines.max().max():
            flashed = flashed | new_nines
            df = new_nines.stack()
            for location in df[df].index:
                for direction in directions:
                    neighbour = location[0] + direction[0], location[1] + direction[1]

                    if neighbour == (0, 1) or location == (0, 2) or location == (1, 1):
                        breakpoint()
                        

                    if (neighbour[0] < 0 or neighbour[1] < 0 or
                        neighbour[0] >= octopi.shape[0] or 
                        neighbour[1] >= octopi.shape[1]):
                        break

                    octopi.loc[neighbour] = octopi.loc[neighbour] + 1
                    #flash_neighbours = pd.DataFrame(morphology.grey_dilation(new_nines, footprint=flash_struc, mode='constant', cval=-1))
                    #print("flashn", flash_neighbours)
                    #breakpoint()
            #breakpoint()
            new_nines = (octopi > 9) & ~flashed
            if debug:
                show_octopi("new nines", new_nines)
                show_octopi("flashed", flashed)
                show_octopi("octopi", octopi)

        octopi[flashed] = 0
        show_octopi(f"End of step {step}", octopi)
        print('-' * 80)
