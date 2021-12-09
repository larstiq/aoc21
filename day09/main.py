#!/usr/bin/env python

import pandas as pd
import numpy as np
import time
with open("simput") as puzzle_input:
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
        print("Basin", ix)
        basins[ix].loc[basin] = True
        print(basins[ix])

    #print(basins)

    #for ix in range(3):
        #    semi_low_mask = ((df <= df.shift(1).fillna(fill_val)) | (df <= df.shift(-1).fillna(fill_val)) |
        #                         (df <= df.shift(1, axis=1).fillna(fill_val)) | (df <= df.shift(-1, axis=1).fillna(fill_val)))
        #print(df[semi_low_mask])
        

    
    covered = df.eq(9) | low_mask
    breakpoint()
    oops = 0
    while not covered.all().all():
        oops = oops + 1
        if oops > 10:
            break
        for semi in [(0, 1), (0, -1), (1, 1), (1, -1)]:
            sh = (~covered).shift(semi[1], axis=semi[0])
            print(df[sh])
            for ix, basin in enumerate(basins):
                found_basin = basin & sh
                #print(found_basin)
                basins[ix][found_basin] = True
                covered = covered | found_basin
                #print(covered)

    
    breakpoint()


    levels = pd.DataFrame(zip(*basin_locations)).T
    for flood_level in range(1, 2):
        flood = df[df == flood_level]
        stacked_flood = flood.stack().dropna()
        for ix, basin in enumerate(basins):
            aap = (pd.DataFrame(zip(*stacked_flood.index)).T - levels.loc[0])
            aap[aap.abs().sum(axis=1) <= 1]
            print("aap", aap.abs().sum())




    if False:
        roundf = 0
        while True:

            stagnants = [False] #* len(basins)
            roundf = roundf + 1
            print("Round", roundf)
            for ix, basin in enumerate(basins):
                if ix == 0:
                    breakpoint()
                obasin = basin.copy()

                growths = []
                for semi in [(0, 1), (0, -1), (1, 1), (1, -1)]:
                    #breakpoint()

                    sh = obasin.shift(semi[1], axis=semi[0])
                    growths.append(df[sh] < 9)

                breakpoint() 

                stagnants[ix] = any(g.any().any() for g in growths)
                grow = growths[0]
                for g in growths:
                    grow = grow | g

                if ix == 0:
                    print(grow)
                    breakpoint()
                basins[ix] = basins[ix] | grow
            if all(stagnants):
                break

    
    # sizes of basins
    cum = 1
    for b in basins:
        size = b.sum().sum()
        cum = cum * size
        print(size)
        print(df[b])
    print(cum)
