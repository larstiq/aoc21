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

segments['slope'] = (segments['y1'] - segments['y0']) / (segments['x1'] - segments['x0'])
print(segments['slope'].value_counts())

def heightmap(diagonal):
    field = pd.DataFrame(data=np.zeros(shape=(xmax + 1, ymax + 1)))
    for ix, (x0, y0, x1, y1, slope) in segments.iterrows():
        x0, y0, x1, y1 = map(int, [x0, y0, x1, y1])
        if abs(slope) == 0 or not np.isfinite(slope):
            # Either x or y is constant, we can just sort both to get increasing coordinates
            a, b = sorted([x0, x1])
            c, d = sorted([y0, y1])
            field.loc[a:b, c:d] = field.loc[a:b, c:d] + 1
        elif diagonal:
            islope = int(slope)
            start, end = sorted([[x0, y0], [x1, y1]])
            cur = start
            field.loc[cur[0], cur[1]] = field.loc[cur[0], cur[1]] + 1
            while cur != end:
                cur[0] = cur[0] + 1
                cur[1] = cur[1] + islope
                field.loc[cur[0], cur[1]] = field.loc[cur[0], cur[1]] + 1
    print(field)
    print(len(field.stack()[field.stack() > 1]))
    return field


heightmap(False)
heightmap(True)
