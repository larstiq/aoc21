#!/usr/bin/env python

import pandas as pd

with open("input") as puzzlein:
    measures = list(map(int, puzzlein))

s = pd.Series(measures)
print(sum(s.diff() > 0))
print(sum(s.rolling(window=3).sum().diff() > 0))
