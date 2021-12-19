#!/usr/bin/env python

import networkx as nx


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


def parse_message(bits, index, tree, parent=None, number_of_packets=None, max_index=None):
    #print("Parsing message of length", len(bits))


    exhausted = False
    parsed_packets = 0
    while not exhausted:
        packet_start = index
        version = int(bits[index:index + 3], 2)
        typeID = bits[index + 3:index + 6]
        index += 6

        if typeID == "100":
            print("literal starting at", index)
            #if index == 108:
                #    breakpoint()
            more = True
            literal = ""
            while more:
                nibble = bits[index:index + 5]
                if len(nibble) != 5:
                    print("NEEEE")
                    #breakpoint()
                if nibble[0] == '0':
                    #breakpoint()
                    more = False
                index += len(nibble)
                literal += nibble[1:]
                #print(int(literal, 2), nibble, more)
                #print(bits)
                #print(bits[:index])
            packet = (version, packet_start, typeID, "literal", int(literal, 2))
            if int(literal, 2) == 15:
                breakpoint()
            tree.add_node(packet)
            parsed_packets += 1
            if parent:
                tree.add_edge(parent, packet)
            else:
                return index, parsed_packets
        else:
            # operator
            length_typeID = bits[index:index + 1]
            index += 1

            if length_typeID == "0":
                total_length = int(bits[index:index + 15], 2)
                index += 15
                packet = (version, packet_start, "operator", typeID, "length", total_length)

                tree.add_node(packet)

                #breakpoint()
                advanced, parsed_subpackets = parse_message(bits, index, tree, packet, max_index=index + total_length)
                index += total_length
                assert index == advanced
                parsed_packets += 1 + parsed_subpackets

                if parent:
                    tree.add_edge(parent, packet)
                else:
                    return index, parsed_packets
            elif length_typeID == "1":
                arg = int(bits[index:index + 11], 2)
                index += 11
                packet = (version, packet_start, "operator", typeID, "number", arg)

                tree.add_node(packet)
                #breakpoint()
                advanced, parsed_subpackets = parse_message(bits, index, tree, packet, number_of_packets=arg)
                index = advanced
                parsed_packets += 1 + parsed_subpackets

                if parent:
                    tree.add_edge(parent, packet)
                else:
                    return advanced, parsed_packets
            else:
                # Bits have run out, why?
                breakpoint()
                return index, parsed_packets



        if (index >= len(bits) or
            (number_of_packets is not None and number_of_packets >= parsed_packets) or
            (max_index is not None and index >= max_index)
           ):
            exhausted = True

    return index, parsed_packets


def go(message):
    bits_list = []
    for hexchar in message:
        bits_list.extend(hex2bin(hexchar))

    bits = "".join(bits_list)


    tree = nx.DiGraph()
    result = parse_message(bits, 0, tree)

    version_sum = sum(n[0] for n in tree.nodes)

    return list(tree.nodes), version_sum


with open("input") as puzzle_input:

    assert [(6, 0, '100', 'literal', 2021)], 6 == go("D2FE28")
    assert [(1, 0, 'operator', '110', 'length', 27), (6, 22, '100', 'literal', 10), (2, 33, '100', 'literal', 20)], 9 == go("38006F45291200")
    assert [(7, 0, 'operator', '011', 'number', 3),
     (2, 18, '100', 'literal', 1),
     (4, 29, '100', 'literal', 2),
     (1, 40, '100', 'literal', 3)], 14 == go("EE00D40C823060")

    assert [(4, 0, 'operator', '010', 'number', 1),
            (1, 18, 'operator', '010', 'number', 1),
            (5, 36, 'operator', '010', 'length', 11),
            (6, 58, '100', 'literal', 15)], 16 == go("8A004A801A8002F478")
    assert [(3, 0, 'operator', '000', 'number', 2),
            (0, 18, 'operator', '000', 'length', 22),
            (0, 40, '100', 'literal', 10),
            (5, 51, '100', 'literal', 11),
            (1, 62, 'operator', '000', 'number', 2),
            (0, 80, '100', 'literal', 12),
            (3, 91, '100', 'literal', 13)], 12 == go("620080001611562C8802118E34")

    assert [(6, 0, 'operator', '000', 'length', 84),
            (0, 22, 'operator', '000', 'length', 22),
            (0, 44, '100', 'literal', 10),
            (6, 55, '100', 'literal', 11),
            (4, 66, 'operator', '000', 'number', 2),
            (7, 84, '100', 'literal', 12),
            (0, 95, '100', 'literal', 13)], 23 == go("C0015000016115A2E0802F182340")

    assert [], 31 == go("A0016C880162017C3686B18A3D4780")
    assert [] == go(puzzle_input.read().strip())
    
