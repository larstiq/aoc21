#!/usr/bin/env python

import pandas as pd

with open("input") as puzzlein:
    measures = list(map(int, puzzlein))

s = pd.Series(measures)
print(s.diff()

print(s.rolling(window=3).diff())
