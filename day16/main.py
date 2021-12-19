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


def parse_message(bits, index, tree, parent=None, number_of_packets=None):
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
            tree.add_node(packet)
            if parent:
                tree.add_edge(parent, packet)
            else:
                return index
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
                advanced = parse_message(bits, index, tree, packet)
                index += total_length

                if parent:
                    tree.add_edge(parent, packet)
                else:
                    return index
            elif length_typeID == "1":
                arg = int(bits[index:index + 11], 2)
                index += 11
                packet = (version, packet_start, "operator", typeID, "number", arg)

                tree.add_node(packet)
                #breakpoint()
                advanced = parse_message(bits, index, tree, packet, number_of_packets=arg)

                if parent:
                    tree.add_edge(parent, packet)
                else:
                    return advanced
            else:
                # Bits have run out, why?
                #breakpoint()
                return index

            parsed_packets += 1

        if (index >= len(bits) or
           (number_of_packets is not None and number_of_packets < parsed_packets)):
            exhausted = True

        return index


def go(message):
    bits_list = []
    for hexchar in message:
        bits_list.extend(hex2bin(hexchar))

    bits = "".join(bits_list)


    tree = nx.DiGraph()
    result = parse_message(bits, 0, tree)
    print(tree.nodes, sum(n[0] for n in tree.nodes))

    return tree.nodes


with open("input") as puzzle_input:

    assert [(6, 0, '100', 'literal', 2021)] == list(go("D2FE28"))
    assert [(1, 0, 'operator', '110', 'length', 27), (6, 22, '100', 'literal', 10)] == list(go("38006F45291200"))
    assert [(7, 0, 'operator', '011', 'number', 3), (2, 18, '100', 'literal', 1)] == list(go("EE00D40C823060"))
    assert [(4, 0, 'operator', '010', 'number', 1), (1, 18, 'operator', '010', 'number', 1), (5, 36, 'operator', '010', 'length', 11), (6, 58, '100', 'literal', 15)] == list(go("8A004A801A8002F478"))
    assert [] == list(go("620080001611562C8802118E34"))
    assert [] == list(go("C0015000016115A2E0802F182340"))
    assert [] == list(go("A0016C880162017C3686B18A3D4780"))
    assert [] == list(go(puzzle_input.read().strip()))
    
