#!/usr/bin/env python

x = 0
depth = 0
aim = 0
with open("input") as inp:
    for line in inp:
        command, arg = line.split()
        if command == "forward":
            x = x + int(arg)
            depth = depth + aim*int(arg)
            if depth < 0:
                print(depth)
        elif command == "down":
            aim = aim + int(arg)
        elif command == "up":
            aim = aim - int(arg)

print(x, depth, x * depth)
