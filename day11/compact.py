#!/usr/bin/env python

import pandas as pd
import numpy as np
import time
from scipy.signal import convolve

# When an octopus flashes it charges all of its neighbours by one
flash_struc = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]], dtype=bool)

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
            weighted_neighours_of_flashes = convolve(
                charged.astype(int), flash_struc, mode='same'
            )

            octopi = octopi + weighted_neighours_of_flashes
            flashed = flashed | charged
            charged = (octopi > 9) & ~flashed

        # After flashing the charge level starts at zero
        octopi[flashed] = 0

        # Keep track of how many octopi flashed this step and in total
        flashes = flashes + flashed.sum().sum()

        if step == 100:
            print("Flashes", flashes)

        synchronized = flashed.all().all()
        if synchronized:
            print("Synchronized at step", step)
