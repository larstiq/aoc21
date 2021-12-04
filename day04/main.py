#!/usr/bin/env python

import pandas as pd
import numpy as np

with open("input") as puzzle_input:
    draws = map(int, puzzle_input.readline().split(","))

    df = pd.read_csv(puzzle_input, delim_whitespace=True, header=None)
    boardslist = [df.iloc[ix:ix + 5].copy() for ix in range(0, len(df), 5)]
    boards = {ix: board for ix, board in enumerate(boardslist)}

    
wins = {}
for ball in draws:
    for ix, board in boards.items():
        if ix in wins:
            continue
        board[board.eq(ball)] = np.nan

        if (board.dropna(how='all', axis=0).shape != board.shape or
            board.dropna(how='all', axis=1).shape != board.shape):
            wins[ix] = (len(wins), ball, board, board.sum().sum() * ball)

print(wins)
