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

    debug = False
    flashes = 0
    dancing = False
    step = 1
    while not dancing:
        flashed = np.zeros_like(octopi, dtype=bool)
        octopi = octopi + 1
        charged = octopi > 9
        show_octopi("after charge", octopi)
        show_octopi("about to flash", charged)

        #breakpoint()
        while charged.any().any():
            df = charged.stack()
            for location in df[df].index:
                for direction in directions:
                    neighbour = location[0] + direction[0], location[1] + direction[1]

                    #if neighbour == (0, 1) or location == (0, 2) or location == (1, 1):
                        #    pass
                        
                    #if neighbour == (0, 1):
                        #    breakpoint()

                    if (neighbour[0] >= 0 and neighbour[1] >= 0 and
                        neighbour[0] < octopi.shape[0] and
                        neighbour[1] < octopi.shape[1]):
                        octopi.loc[neighbour] = octopi.loc[neighbour] + 1
                    #flash_neighbours = pd.DataFrame(morphology.grey_dilation(new_nines, footprint=flash_struc, mode='constant', cval=-1))
                    #print("flashn", flash_neighbours)
                    #breakpoint()
                    #breakpoint()
            flashed = flashed | charged
            charged = (octopi > 9) & ~flashed
            if debug:
                show_octopi("new nines", charged)
                show_octopi("flashed", flashed)
                show_octopi("octopi", octopi)

        octopi[flashed] = 0
        flashes = flashes + flashed.sum().sum()
        print("Flashes", flashes)
        show_octopi(f"End of step {step}", octopi)
        print('-' * 80)
        step = step + 1
        dancing = flashed.all().all()
