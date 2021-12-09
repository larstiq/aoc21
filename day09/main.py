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


