#!/usr/bin/env python


def hex2bin(c):
    mapping = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }
    return mapping[c]


with open("input") as puzzle_input:

    message = puzzle_input.read().strip()
    message = "D2FE28"

    bits_list = []
    for c in message:
        bits_list.extend(hex2bin(c))

    bits = "".join(bits_list)

    
    version = bits[:3]
    typeID = bits[3:6]
    index = 6

    if typeID == "100":
        more = True
        literal = ""
        while more:
            nibble = bits[index:index + 5]
            if nibble[0] == '0':
                more = False
            index += 5
            literal += nibble[1:]
            print(literal, nibble, more)


    print(message)


