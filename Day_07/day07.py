#!/usr/bin/env python3

"""
    <color> bags contain <number> <color> bag(s) [, <number> <color> bag(s)]*.
"""

from parse import *


def parse_line(line):
    #print(f"{line}")
    # easy case: no other bags
    p = parse("{outer} bags contain no other bags.", line)
    if p:
        return p['outer'], {}
    p = parse("{outer} bags contain {bags}.", line)
    outer = p['outer']
    text = p['bags']
    results = {}
    for i in text.split(', '):
        p = parse("{number:d} {color} bag", i.strip().rstrip('s'))
        if not p:
            print("ERROR")
            exit(-1)
        results[p['color']] = p['number']
    return outer, results


def find_bags(can_contain, in_outer, target):
    for color, number in can_contain[in_outer].items():
        if color == target:
            return True
        if find_bags(can_contain, color, target):
            return True
    return False


def count_sub_bags(can_contain, target):
    count = 0
    for color, number in can_contain[target].items():
        count += number
        if number > 0:
            count += (number * count_sub_bags(can_contain, color))
    return count


with open("input", "rt") as f:
    lines = f.readlines()

print(f'{len(lines)} lines read.')

can_contain = {}  # dict of color -> dict(color -> number)
for line in lines:
    color, contents = parse_line(line.strip())
    can_contain[color] = contents

print(f'{len(can_contain)} rules.')

count = 0
for outer, rules in can_contain.items():
    count += 1 if find_bags(can_contain, outer, 'shiny gold') else 0
    
print(f"{count} colors can contain 'shiny gold'")

# PART 2 how many bags must shiny gold contain?
count = count_sub_bags(can_contain, 'shiny gold')
print(f"{count} bags in 'shiny gold'")

# vim: sw=4:ts=4:ai:et
