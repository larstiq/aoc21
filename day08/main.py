#!/usr/bin/env python

import pandas as pd
import numpy as np
import time

with open("input") as puzzle_input:
    wires = pd.read_csv(puzzle_input, delim_whitespace=True, header=None)
    # TODO: assert wires[10] == '1'



#     0:      1:      2:      3:      4:
#    aaaa    ....    aaaa    aaaa    ....
#   b    c  .    c  .    c  .    c  b    c
#   b    c  .    c  .    c  .    c  b    c
#    ....    ....    dddd    dddd    dddd
#   e    f  .    f  e    .  .    f  .    f
#   e    f  .    f  e    .  .    f  .    f
#    gggg    ....    gggg    gggg    ....
#
#     5:      6:      7:      8:      9:
#    aaaa    aaaa    aaaa    aaaa    aaaa
#   b    .  b    .  .    c  b    c  b    c
#   b    .  b    .  .    c  b    c  b    c
#    dddd    dddd    ....    dddd    dddd
#   .    f  e    f  .    f  e    f  .    f
#   .    f  e    f  .    f  e    f  .    f
#    gggg    gggg    ....    gggg    gggg

outputs = wires[[11, 12, 13, 14]]
counts = pd.DataFrame()

for column in outputs:
    counts[column] = outputs[column].map(len)


easy_digits = (counts < 5) | (counts > 6)

print(outputs)
print(counts)
print(easy_digits.sum().sum())
