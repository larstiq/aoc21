
import pandas as pd
import numpy as np
from collections import Counter
import itertools

with open("input") as puzzle_input:
    players = pd.Series(int(line.split(":")[1].strip()) for line in puzzle_input) - 1
    board = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    score = np.zeros_like(players)
    playdex = 0
    print(players)

    score = np.zeros_like(players)
    universes = Counter()
    universes[(tuple(score), tuple(players))] = 1

    done_verses = Counter()
    while not all((score[0] >= 21 or score[1] >= 21) for (score, players) in universes):
        new_universes = Counter()
        unfinished = 0
        finished = 0
        for universe in universes:
            count = universes[universe]

            if universe[0][0] >= 21 or universe[0][1] >= 21:
                done_verses[universe] += count
                finished += count
                continue

            unfinished += count

            for roll in itertools.product([1, 2, 3], [1, 2, 3], [1, 2, 3]):
                score, players = map(pd.Series, universe)
                advance = sum(roll)
                players[playdex] = (players[playdex] + advance) % len(board)
                score[playdex] += board[players[playdex]]

                new_universes[(tuple(score), tuple(players))] += count

        playdex = (playdex +  1) % len(players)
        universes = new_universes
        print(finished, unfinished)

    for verse in universes:
        done_verses[verse] += universes[verse]

    won_one = sum(count for (score, players), count in done_verses.items() if score[0] >= 21)
    won_two = sum(count for (score, players), count in done_verses.items() if score[1] >= 21)
    print(won_one, won_two, max(won_one, won_two))




def deterministic(players, score):
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


