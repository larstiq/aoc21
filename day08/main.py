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


signals = wires[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]

res = 0
for ix, row in wires.iterrows():
    mapping = [None] * 10
    row_signals = row[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
    lens = row_signals.map(len)
    mapping[1] = row_signals[lens.eq(2)].to_list()[0]
    mapping[4] = row_signals[lens.eq(4)].to_list()[0]
    mapping[7] = row_signals[lens.eq(3)].to_list()[0]
    mapping[8] = row_signals[lens.eq(7)].to_list()[0]

    zero_six_nine = row_signals[lens.eq(6)]

    nine, = zero_six_nine[zero_six_nine.map(lambda x: set(mapping[4] + mapping[7]).issubset(x))].to_list()
    zero, = set(zero_six_nine[zero_six_nine.map(lambda x: set(mapping[1]).issubset(x))].to_list()) - set([nine])
    six, = set(zero_six_nine) - set([zero, nine])
    mapping[0] = zero
    mapping[6] = six
    mapping[9] = nine

    two_three_five = set(row_signals) - set(mapping)

    five, = [n for n in two_three_five if set(n).issubset(six) ]
    two, = [n for n in two_three_five if (set('abcdefg') - set(nine)).issubset(set(n))]
    three, = two_three_five - set([two, five])

    mapping[2] = two
    mapping[3] = three
    mapping[5] = five

    mapping_to_digit = {''.join(sorted(mapping[ix])): str(ix) for ix in range(10)}
    row_outputs = row[[11, 12, 13, 14]]
    digits = row_outputs.map(lambda x: mapping_to_digit[''.join(sorted(x))])

    res = res + int(''.join(digits))


print(res)
