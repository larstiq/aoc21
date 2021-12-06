#!/usr/bin/env python

import pandas as pd
import numpy as np

segments = []
with open("input") as puzzle_input:
    fishes = pd.read_csv(puzzle_input, header=None).transpose()
    print(fishes)

for day in range(80):
    fishes = (fishes - 1)
    birthing_fishes = fishes < 0
    #print("after dec", fishes.transpose().values)
    #print("birthing", birthing_fishes.values)
    #print("nbirthing", birthing_fishes.sum())
    fishes[birthing_fishes] = 6
    fishes = fishes.append([8] * birthing_fishes.sum().sum(), ignore_index=True)
    print(fishes.transpose().values)
    #print("fater birth:", fishes.transpose().values)
            

