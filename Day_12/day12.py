#!/usr/bin/env python3

from parse import *

from collections import namedtuple


def part1(filename):
    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"Part 1, {filename}, {len(lines)} lines")

    Pos = namedtuple('Position', ['x', 'y', 'angle'])

    directions = {  # (x, y) for moves and angles, positive or negative number for rotation
        'N': (0, -1),
        'S': (0, 1),
        'E': (1, 0),
        'W': (-1, 0),
        0: (0, -1),
        180: (0, 1),
        90: (1, 0),
        270: (-1, 0),
        'L': -1,
        'R': 1,
    }

    def move(pos, op, value):
        return Pos(pos.x + directions[op][0] * value, pos.y + directions[op][1] * value, pos.angle)
        
    def rotate(pos, op, value):
        return Pos(pos.x, pos.y, (pos.angle + directions[op] * value) % 360)

    def forward(pos, op, value):
        return Pos(pos.x + directions[pos.angle][0] * value, pos.y + directions[pos.angle][1] * value, pos.angle)

    ops = {
       'N': move,
       'S': move,
       'E': move,
       'W': move,
       'L': rotate,
       'R': rotate,
       'F': forward,
    }

    pos = Pos(0, 0, 90)  # position 0,0, pointing east
    print(f"Start: {pos}")

    for line in lines:
        p = parse("{op:l}{value:d}", line)
        pos = ops[p['op']](pos, p['op'], p['value'])
        # print(f'Step:  {line:10s} {pos}')

    print(f'End:   {pos} manhattan: {abs(pos.x) + abs(pos.y)}\n')


def part2(filename):
    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"Part 2, {filename}, {len(lines)} lines")

    Pos = namedtuple('Position', ['x', 'y', 'wx', 'wy']) # (x,y) for boat and relative (wx,wy) for waypoint

    directions = {
        'N': (0, -1),
        'S': (0, 1),
        'E': (1, 0),
        'W': (-1, 0),
        'L': -1,
        'R': 1,
    }

    def move(pos, op, value):
        return Pos(pos.x, pos.y, pos.wx + directions[op][0] * value, pos.wy + directions[op][1] * value)
        
    def rotate(pos, op, value):
        angle = (value * directions[op]) % 360
        angles = {
            0:  (pos.wx, pos.wy),
            90: (-pos.wy, pos.wx),
            180: (-pos.wx, -pos.wy),
            270: (pos.wy, -pos.wx),
        }
        return Pos(pos.x, pos.y, angles[angle][0], angles[angle][1])
    
    def forward(pos, op, value):
        return Pos(pos.x + pos.wx * value, pos.y + pos.wy * value, pos.wx, pos.wy)


    ops = {
       'N': move,
       'S': move,
       'E': move,
       'W': move,
       'L': rotate,
       'R': rotate,
       'F': forward,
    }

    pos = Pos(0, 0, 10, -1)  # position 0,0, waypoint at 10,-1
    print(f"Start: {pos}")
    
    for line in lines:
        p = parse("{op:l}{value:d}", line)
        pos = ops[p['op']](pos, p['op'], p['value'])
        # print(f'Step:  {line:10s} {pos}')

    print(f'End:   {pos} manhattan: {abs(pos.x) + abs(pos.y)}\n')


def main():
    part1('demo-input')
    part1('input')

    part2('demo-input')
    part2('input')

if __name__ == '__main__':
    main()

# vim: et:ai:sw=4:ts=4
