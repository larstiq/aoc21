#!/usr/bin/env python


def hex2bin(hexchar):
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
    return mapping[hexchar]


def parse_message(bits, total_length=None, number_of_packets=None):
    if bits == '':
        breakpoint()
    index = 6


    exhausted = False
    while not exhausted:
        version = int(bits[:3], 2)
        typeID = bits[3:6]

        if typeID == "100":
            more = True
            literal = ""
            while more:
                nibble = bits[index:index + 5]
                if nibble[0] == '0':
                    more = False
                index += len(nibble)
                literal += nibble[1:]
                print(int(literal, 2), nibble, more)
            packet = (version, typeID, literal)
            subpackets = []
        else:
            # operator
            length_typeID = bits[index:index + 1]
            index += 1

            if length_typeID == "0":
                arg = int(bits[index:index + 15], 2)
                index += 15
                packet = (version, "operator", typeID, "length", arg)
                breakpoint()
                subpackets = parse_message(bits[index:], total_length=arg)
            elif length_typeID == "1":
                arg = int(bits[index:index + 11], 2)
                index += 11
                packet = (version, "operator", typeID, "number", arg)
                breakpoint()
                subpackets = parse_message(bits[index:], number_of_packets=arg)
            else:
                breakpoint()

        if (index >= len(bits) or
           (total_length is not None and total_length < index) or
           (number_of_packets is not None and number_of_packets < len(subpackets))):
            exhausted = True



    return [packet] + subpackets



with open("input") as puzzle_input:

    message = puzzle_input.read().strip()
    message = "D2FE28"
    message = "38006F45291200"

    bits_list = []
    for hexchar in message:
        bits_list.extend(hex2bin(hexchar))

    bits = "".join(bits_list)


    result = parse_message(bits)
    
