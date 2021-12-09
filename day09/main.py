#!/usr/bin/env python

import pandas as pd
import numpy as np
import time

with open("input") as puzzle_input:
    data = [list(map(int, line.strip())) for line in puzzle_input]
    df = pd.DataFrame(data=data)

    fill_val = df.max().max() + 1
    low_mask_hoz = (df < df.shift(1).fillna(fill_val)) & (df < df.shift(-1).fillna(fill_val))
    low_mask_vert = (df < df.shift(1, axis=1).fillna(fill_val)) & (df < df.shift(-1, axis=1).fillna(fill_val))
    
    low_mask = low_mask_hoz & low_mask_vert
    low_risk = df[low_mask] + 1

    risk = df + 1

    print(low_risk.sum().sum())
    print(df[low_mask])

    oned = low_mask.stack()
    oned[oned == False] = np.nan
    basin_locations = oned.dropna().index
    
    basin_sets = {
        ix: set([l]) for ix, l in enumerate(basin_locations)
    }

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

    cum = 1
    for size in sorted(sizes.values())[-3:]:
        cum = cum * size
    print(cum)
    #functools.reduce(operator.mul, sorted(sizes.values())[-3:], 1)
