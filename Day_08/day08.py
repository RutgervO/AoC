#!/usr/bin/env python3

from parse import *

with open('input', 'rt') as f:
    lines = list(f)
print(f"{len(lines)} lines read")

acc_action = {
    'acc': lambda v: v,
    'jmp': lambda v: 0,
    'nop': lambda v: 0
}
pos_action = {
    'acc': lambda v: 1,
    'jmp': lambda v: v,
    'nop': lambda v: 1
}

acc = 0
pos = 0
used = set()

while True:
    line = lines[pos]
    # print(f"{pos} {acc} {line}")
    if pos in used:
        print(f'Boom - pos {pos} would be run again. acc {acc}')
        break
    used.add(pos)
    instruction = line[0:3]
    p = parse("{num:d}", line[4:])
    number = p['num']
    acc += acc_action[instruction](number)
    pos += pos_action[instruction](number)

####part2

permlines = [i for i in range(0,len(lines)) if lines[i][0:3] in {'nop', 'jmp'}]
permutate = {
    'acc': 'acc',
    'jmp': 'nop',
    'nop': 'jmp'
}

def run_to_finish(lines, permpos):
    acc = 0
    pos = 0
    used = set()

    while not pos >= len(lines):
        line = lines[pos]
        if pos in used:
            return False # CRASH
        used.add(pos)
        instruction = line[0:3]
        if pos == permpos:
            instruction = permutate[instruction]
        p = parse("{num:d}", line[4:])
        number = p['num']
        acc += acc_action[instruction](number)
        pos += pos_action[instruction](number)
    print(f'Permpos {permpos} finishes with acc {acc}')
    return True # Finish!

for permpos in permlines:
    run_to_finish(lines, permpos)

# vim: ai:sw=4:ts=4:et
