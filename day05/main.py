#!/usr/bin/env python

import pandas as pd
import numpy as np

segments = []
with open("input") as puzzle_input:
    for line in puzzle_input:
        if line == "\n":
            continue
        x0y0, x1y1 = [end.strip().split(",") for end in line.strip().split("->")]
        segments.append(list(map(int, x0y0)) + list(map(int, x1y1)))


segments = pd.DataFrame(data=segments, columns=["x0", "y0", "x1", "y1"])

xmax = segments[['x1', 'x0']].max().max()
ymax = segments[['y1', 'y0']].max().max()

field = pd.DataFrame(data=np.zeros(shape=(xmax + 1, ymax + 1)))

segments['slope'] = (segments['y1'] - segments['y0']) / (segments['x1'] - segments['x0'])
# assert all integer

for ix, (x0, y0, x1, y1, slope) in segments.iterrows():
    x0, y0, x1, y1 = map(int, [x0, y0, x1, y1])
    if abs(slope) == 0 or not np.isfinite(slope):
        # Either x or y is constant, we can just sort both to get increasing coordinates
        a, b = sorted([x0, x1])
        c, d = sorted([y0, y1])
        field.loc[a:b, c:d] = field.loc[a:b, c:d] + 1

print(len(field.stack()[field.stack() > 1]))
