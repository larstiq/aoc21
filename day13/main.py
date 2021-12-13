#!/usr/bin/env python

import pandas as pd
import numpy as np


def display(shape):
    output = pd.DataFrame(data=shape)
    output[shape == False] = "."
    output[shape == True] = "#"
    print(output.T)

with open("simput") as puzzle_input:
    x_coords = []
    y_coords = []
    folds = []
    for line in puzzle_input:
        if "," in line:
            x, y = line.strip().split(",")
            x_coords.append(int(x))
            y_coords.append(int(y))
        elif "fold along" in line:
            folds.append(line.strip().split("="))
        else:
            if line == "\n":
                continue
            else:
                breakpoint()


    df = np.zeros(shape=(max(y_coords) +1, max(x_coords) + 1), dtype=bool)
    for x, y in zip(x_coords, y_coords):
        df[y, x] = True

    odf = df
    print(df)
    
    for fold in folds:
        #for fold in folds:
        if fold[0].endswith("y"):
            fold_y = int(fold[1])
            # We should not include the fold
            half1 = df[:fold_y, :]
            half2 = df[fold_y + 1:, :]
            if half1.shape != half2.shape:
                print("no shape match", half1.shape, half2.shape)
                #breakpoint()

                diff = half1.shape[0] - half2.shape[0]
                bufferr = np.zeros(shape=(abs(diff), half2.shape[1]), dtype=bool)
                if diff < 0:
                    breakpoint()
                    half1 = np.concatenate([half1, bufferr], axis=0)
                else:
                    half2 = np.concatenate([half2, bufferr], axis=0)
            df = half1 | np.flip(half2, axis=0)
            print(df.shape)
        else:
            breakpoint()
            fold_x = int(fold[1])
            half1 = df[:, :fold_x]
            half2 = df[:, fold_x + 1:]
            if half1.shape != half2.shape:
                print("no shape match", half1.shape, half2.shape)
                #breakpoint()
                diff = half1.shape[1] - half2.shape[1]
                bufferr = np.zeros(shape=(half2.shape[0], abs(diff)), dtype=bool)

                if diff < 0:
                    breakpoint()
                    half1 = np.concatenate([half1, bufferr], axis=1)
                else:
                    half2 = np.concatenate([half2, bufferr], axis=1)
            df = half1 | np.flip(half2, axis=1)
            print(df.shape)

        display(df)


    display(df)



