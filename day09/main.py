#!/usr/bin/env python

import pandas as pd
import numpy as np
import time
with open("input") as puzzle_input:
    data = [list(map(int, line.strip())) for line in puzzle_input]
    print(data)
    # TODO: assert wires[10] == '1'
    df = pd.DataFrame(data=data)
    print(df)

    fill_val = df.max().max() + 1
    low_mask_hoz = (df < df.shift(1).fillna(fill_val)) & (df < df.shift(-1).fillna(fill_val))
    low_mask_vert = (df < df.shift(1, axis=1).fillna(fill_val)) & (df < df.shift(-1, axis=1).fillna(fill_val))
    
    low_mask = low_mask_hoz & low_mask_vert
    low_risk = df[low_mask] + 1

    risk = df + 1
    print(low_risk.sum().sum())


    semi_low_mask = ((df <= df.shift(1).fillna(fill_val)) & (df <= df.shift(-1).fillna(fill_val)) &
                     (df <= df.shift(1, axis=1).fillna(fill_val)) & (df <= df.shift(-1, axis=1).fillna(fill_val)))


    print(df[low_mask])

    basins = df[semi_low_mask]

    semis = [
        (df <= df.shift(1).fillna(fill_val)),
        (df <= df.shift(-1).fillna(fill_val)),
        (df <= df.shift(1, axis=1).fillna(fill_val)),
        (df <= df.shift(-1, axis=1).fillna(fill_val))
    ]

    #for ix, semi in enumerate(semis):
        #    print(ix, '-' * 80)
        #print(df[semi])

    oned = low_mask.stack()
    oned[oned == False] = np.nan
    basin_locations = oned.dropna().index
    
    basins = [pd.DataFrame(index=df.index, columns=df.columns, data=False) for ix in basin_locations]
    for ix, basin in enumerate(basin_locations):
        #print("Basin", ix)
        basins[ix].loc[basin] = True
        #print(basins[ix])

    #print(basins)

    #for ix in range(3):
        #    semi_low_mask = ((df <= df.shift(1).fillna(fill_val)) | (df <= df.shift(-1).fillna(fill_val)) |
        #                         (df <= df.shift(1, axis=1).fillna(fill_val)) | (df <= df.shift(-1, axis=1).fillna(fill_val)))
        #print(df[semi_low_mask])
        

    basin_sets = {
        ix: set([l]) for ix, l in enumerate(basin_locations)
    }

    
    covered = df.eq(9) | low_mask
    oops = 0
    while not covered.all().all():
        oops = oops + 1
        if oops > 10:
            break

        for neighbour in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            for cell in df[~covered].stack().index:
                for ix in basin_sets:
                    if (cell[0] + neighbour[0], cell[1] + neighbour[1]) in basin_sets[ix]:
                        #breakpoint()
                        basin_sets[ix].add(cell)
                        covered.loc[cell] = True
                        #print(basin_sets)

    
    
    sizes = {
        ix: len(basin_sets[ix]) for ix in basin_sets
    }
    # sizes of basins
    cum = 1
    for size in sorted(sizes.values())[-3:]:
        cum = cum * size
    print(cum)

