#!/usr/bin/env python3.10

import itertools
from collections import Counter

pairs = {}
with open("input") as puzzle_input:
    polymer = list(puzzle_input.readline().strip())
    puzzle_input.readline()
    for line in puzzle_input:
        left, right = line.strip().split(" -> ")
        pairs[tuple(left)] = right

    char_count = Counter(polymer)
    polymer_count = Counter()

    for pair in itertools.pairwise(polymer):
        polymer_count[pair] += 1

    for step in range(40):
        new_polymer = Counter()
        for pair in polymer_count:


            count = polymer_count[pair]
            insert_char = pairs[pair]
            new_polymer[(pair[0], insert_char)] += count
            new_polymer[(insert_char, pair[1])] += count
            char_count[insert_char] += count

        polymer_count = new_polymer

    print(polymer_count)
    print(char_count.most_common()[0][1] - char_count.most_common()[-1][1])
