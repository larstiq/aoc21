#!/usr/bin/env python

import networkx as nx
import pandas as pd
import numpy as np
from math import ceil
from scipy.spatial import ConvexHull


with open("input") as puzzle_input:
    instructions = puzzle_input.read().strip()
    assert instructions.startswith("target area: ")
    coords = instructions[len("target area: ") :]

    x_target, y_target = [
        tuple(map(int, c.split("=")[1].split(".."))) for c in coords.split(", ")
    ]
    assert x_target[0] < x_target[1]
    assert y_target[0] < y_target[1]

    print(x_target, y_target)

    oneshot_cone = ConvexHull(
        [
            (0, 0),
            (x_target[0], y_target[1]),
            (x_target[1], y_target[1]),
            (x_target[1], y_target[0]),
        ]
    )

    print(oneshot_cone)

    # We should be able to restrict the search space, but an outer approximation is the square given
    # by origin and the furthest away vertex of the target area, plus something above to account for gravity


    def trajectory(init_vx, init_vy):

        if (init_vx, init_vy) in [
            (7, 2),
            (6, 3),
            (9, 0),
            (6, 9),
            (17, 4),
        ]:
            pass
        #breakpoint()

        if (init_vx, init_vy) in [
            (6, 0),
        ]:
            pass

        hit = False
        position = 0, 0
        vx, vy = init_vx, init_vy

        positions = [position]
        while position[0] <= x_target[1] and position[1] >= y_target[0]:
            position = position[0] + vx, position[1] + vy
            positions.append(position)
            
            if position == (18, -6):
                if (init_vx, init_vy) in [
                    (6, 0),
                ]:
                    pass #breakpoint()

            if (x_target[0] <= position[0] <= x_target[1] and
                y_target[0] <= position[1] <= y_target[1]):
                hit = True
                break


            if vx > 0:
                vx = vx - 1
            elif vx < 0:
                vx = vx + 1
            else:
                vx = 0

            vy = vy - 1

        return positions, hit


    # Drag reduces the x component by 1 every step, so we have at maximum v_x steps to reach
    # the target x area. Ground covered is v_x + (v_x - 1) + (v_x - 2) + ... = v_x*(v_x + 1)/2
    # Slowest x we can shoot with is then
    #
    #    x_target[0]  = v_x*(v_x + 1)/2

    # Very rough bounds for x are roots of polynomial
    #
    #     0.5 x^2 + 0.5 x - x_target[0]  (= 0)
    #
    #
    max_permissible_x = x_target[1]
    poly = np.polynomial.Polynomial([-x_target[0], 0.5, 0.5])
    roots = poly.roots()

    poly2 = np.polynomial.Polynomial([-x_target[1], 0.5, 0.5])
    roots2 = poly2.roots()
    # We need the smallest positive root. Only integer launching, so ceil that.
    min_permissible_x = ceil(min(r for r in roots if r > 0))
    mid_permissible_x = ceil(min(r for r in roots2 if r > 0))

    # How many steps are taken between these two parabolas that reach left and right corners?
    # 
    # If we were not doing integers the
    #
    
    

    # Gravity reduces y component by 1 every step, to reach target area we get
    #
    #   v_y + (v_y - 1) + (v_y - 2) + ... 
    #
    #  Most negative we can choose is y_target[1], anything beyond that and the initial shot already 
    #  places it outside


    min_permissible_v = y_target[1]

    permissible_v = [
        (vx, vy) for vx in range(min_permissible_x, max_permissible_x + 1)
            for vy in range(y_target[0], 1000)
    ]



    best_v = None
    max_height = y_target[1]
    covered = set([])
    hits = set([])
    for v in permissible_v:
        #print("Considering v", v)

        covered.add(v)
        # Can not shoot higher than best option if lower velocity
        # TODO: shrink permissible set
        if False and best_v:
            if v[1] < best_v[1]:
                continue

        path, hit = trajectory(*v)
        if hit:
            hits.add(v)
            height = max(p[1] for p in path)
            print(v, path, hit, height)

            if max_height < height:
                max_height = height


    wats = [
        (23,-10), (25,-9),  (27,-5 ), (29,-6 ), (22,-6),  (21,-7 ), (9,0   ), (27,-7 ), (24,-5 ),
        (25,-7 ), (26,-6),  (25,-5 ), (6,8   ), (11,-2),  (20,-5 ), (29,-10), (6,3   ), (28,-7),
        (8,0   ), (30,-6),  (29,-8 ), (20,-10), (6,7  ),  (6,4   ), (6,1   ), (14,-4 ), (21,-6),
        (26,-10), (7,-1 ),  (7,7   ), (8,-1  ), (21,-9),  (6,2   ), (20,-7 ), (30,-10), (14,-3),
        (20,-8 ), (13,-2),  (7,3   ), (28,-8 ), (29,-9),  (15,-3 ), (22,-5 ), (26,-8 ), (25,-8),
        (25,-6 ), (15,-4),  (9,-2  ), (15,-2 ), (12,-2),  (28,-9 ), (12,-3 ), (24,-6 ), (23,-7),
        (25,-10), (7,8  ),  (11,-3 ), (26,-7 ), (7,1  ),  (23,-9 ), (6,0   ), (22,-10), (27,-6),
        (8,1   ), (22,-8),  (13,-4 ), (7,6   ), (28,-6),  (11,-4 ), (12,-4 ), (26,-9 ), (7,4),
        (24,-10), (23,-8),  (30,-8 ), (7,0   ), (9,-1 ),  (10,-1 ), (26,-5 ), (22,-9 ), (6,5),
        (7,5   ), (23,-6),  (28,-10), (10,-2 ), (11,-1),  (20,-9 ), (14,-2 ), (29,-7 ), (13,-3),
        (23,-5 ), (24,-8),  (27,-9 ), (30,-7 ), (28,-5),  (21,-10), (7,9   ), (6,6   ), (21,-5),
        (27,-10), (7,2  ),  (30,-9 ), (21,-8 ), (22,-7),  (24,-9 ), (20,-6 ), (6,9   ), (29,-5),
        (8,-2  ), (27,-8),  (30,-5 ), (24,-7),
    ]
    print(len(hits), hits)
