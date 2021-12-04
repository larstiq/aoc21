#!/usr/bin/env python

import pandas as pd

with open("input") as inp:
    lines = []
    for line in inp:
        lines.append(list(line.strip()))

    gamma = []
    epsilon = []
    for bit in zip(*lines):
        s = pd.Series(bit)
        g, e = s.value_counts().index
        gamma.append(g)
        epsilon.append(e)

    gi = int("".join(gamma), 2)
    ei = int("".join(epsilon), 2)
    print(gi * ei)
