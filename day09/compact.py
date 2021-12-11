#!/usr/bin/env python

from functools import reduce
from operator import mul

import numpy as np
import pandas as pd
from scipy.ndimage import measurements, grey_erosion


with open("input") as puzzle_input:
    data = [list(map(int, line.strip())) for line in puzzle_input]
    df = pd.DataFrame(data=data)

    mountain_height = df.max().max()
    neighbourhood = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=bool)
    lowest_neighbours = grey_erosion(
        df, footprint=neighbourhood, mode="constant", cval=mountain_height + 1
    )
    low_points = df < lowest_neighbours
    risk = (df + 1)[low_points].sum().sum()
    print(risk)

    nonmountains = df < mountain_height
    terrain_by_basin, n_basins = measurements.label(nonmountains)
    basins = {label: terrain_by_basin == label for label in range(1, n_basins + 1)}
    sizes = {label: basin.sum(axis=None) for label, basin in basins.items()}

    print(reduce(mul, sorted(sizes.values())[-3:], 1))
