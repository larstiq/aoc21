
import pandas as pd
import numpy as np
with open("input") as puzzle_input:
    players = pd.Series(int(line.split(":")[1].strip()) for line in puzzle_input) - 1
    board = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    score = np.zeros_like(players)
    print(players)

    die = list(range(1, 100 + 1))
    diedex = 0
    playdex = 0

    rolls = 0
    while score.max() < 1000:
        roll = die[diedex:diedex + 3]
        diedex = (diedex + 3) % 100 
        if len(roll) < 3:
            breakpoint()
            roll += die[0:diedex]

        rolls += 3
        
        advance = sum(roll)
        players[playdex] = (players[playdex] + advance) % len(board)
        score[playdex] += board[players[playdex]]
        playdex = (playdex +  1) % len(players)

        print(score)


    print(rolls * score.min())
