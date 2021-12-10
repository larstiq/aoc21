#!/usr/bin/env python

import pandas as pd
import numpy as np
import time

OPENS = "([{<"
CLOSES = ")]}>"

score_mapping = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

completion_mapping = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


illegals = []
completions = []
with open("input") as puzzle_input:
    for line in puzzle_input:
        stack = []
        for char in line:
            if char in OPENS:
                stack.append(char)
            elif char in CLOSES:
                if OPENS.find(stack[-1]) == CLOSES.find(char):
                    stack.pop()
                else:
                    illegals.append(char)
                    break
        else:
            completion = "".join(reversed(stack))
            completion_score = 0
            for char in completion:
                completion_score = completion_score * 5 + completion_mapping[char]

            completions.append((completion_score, completion))

    print(sorted(completions)[int(len(completions)/2)])
    score = sum(score_mapping[char] for char in illegals)
    print(score)

