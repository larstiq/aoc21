#!/usr/bin/env python

import pandas as pd

with open("input") as inp:
    lines = []
    for line in inp:
        lines.append(list(line.strip()))

    df = pd.DataFrame({ix: bit for ix, bit in enumerate(zip(*lines))})

    oxygen = df.copy()
    co2 = df.copy()

    for c in df.columns:
        if len(oxygen) > 1:
            obit = oxygen[c].value_counts().index[0]
            oxygen = oxygen[oxygen[c] == obit]

        if len(co2) > 1:
            cbit = co2[c].value_counts().index[1]
            co2 = co2[co2[c] == cbit]

    oi = int("".join(oxygen.iloc[0]), 2)
    ci = int("".join(co2.iloc[0]), 2)
    print(oi * ci)
