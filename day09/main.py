#!/usr/bin/env python

import time
import pandas as pd
import numpy as np
from functools import reduce
from operator import mul

from scipy.ndimage import measurements
from scipy.ndimage import grey_erosion

with open("input") as puzzle_input:
    data = [list(map(int, line.strip())) for line in puzzle_input]
    df = pd.DataFrame(data=data)

    mountain_height = df.max().max()
    fill_val = mountain_height + 1

    def byhand():
        start = time.time()
        # Lowest points are those locations where all of their neighbours are
        # higher. Extend the boundary with a value higher than anything else.

        low_mask_hoz = (df < df.shift(1).fillna(fill_val)) & (
            df < df.shift(-1).fillna(fill_val)
        )
        low_mask_vert = (df < df.shift(1, axis=1).fillna(fill_val)) & (
            df < df.shift(-1, axis=1).fillna(fill_val)
        )

        low_mask = low_mask_hoz & low_mask_vert
        low_risk = df[low_mask] + 1

        print(low_risk.sum().sum())

        # Everything but the low points
        oned = low_mask.stack()
        oned[oned == False] = np.nan
        basin_locations = oned.dropna().index

        basin_sets = {ix: set([l]) for ix, l in enumerate(basin_locations)}

        # Find the basins by iterating over the points we have not seen yet and
        # checking whether their neighbours are part of a known basin. Slow.
        covered = df.eq(9) | low_mask
        while not covered.all().all():
            for direction in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                for cell in df[~covered].stack().index:
                    for ix in basin_sets:
                        neighbour = (cell[0] + direction[0], cell[1] + direction[1])
                        if neighbour in basin_sets[ix]:
                            basin_sets[ix].add(cell)
                            covered.loc[cell] = True

        sizes = dict((ix, len(basin_sets[ix])) for ix in basin_sets)
        score(sizes)
        print(time.time() - start)

    def byscipy():
        start = time.time()
        # Lowest points are those locations where all of their neighbours are
        # higher. Find them by:
        #
        # 1) calculating the lowest neighbour per point,
        neighbourhood = np.array(
            [[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=bool
        )  # neighbours are hor/ver, not diag
        lowest_neighbours = grey_erosion(
            df, footprint=neighbourhood, mode="constant", cval=mountain_height + 1
        )

        # 2) selecting locations lower than their lowest neighbour
        low_points = df < lowest_neighbours

        # How risky are these lowpoints?
        risk = (df + 1)[low_points].sum().sum()
        print(risk)

        # Find basins by segmenting the map into connected components separated by
        # the highest mountains
        nonmountains = df < mountain_height
        terrain_by_basin, n_basins = measurements.label(nonmountains)
        basins = {label: terrain_by_basin == label for label in range(1, n_basins + 1)}
        sizes = {label: basin.sum(axis=None) for label, basin in basins.items()}
        score(sizes)
        print(time.time() - start)

    def score(sizes):
        cum = 1
        biggest = sorted(sizes.values())[-3:]
        for size in biggest:
            cum = cum * size
        print(cum)

        # Or
        r = reduce(mul, biggest, 1)
        print(r)

    byscipy()
    byhand()
