#!/usr/bin/env python3

from parse import *


def part1(filename):
    print(f"Part 1, reading {filename}")
    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"{len(lines)} read")

    status = (0,0), 90  # position 0,0, pointing east

    def move(status, op, value):
        (sx, sy), sa = status
        directions = {
            'N': (0, -1),
            'S': (0, 1),
            'E': (1, 0),
            'W': (-1, 0),
        }
        dx, dy = directions[op]
        sx += dx * value
        sy += dy * value
        return (sx, sy), sa
        
    def rotate(status, op, value):
        (sx, sy), sa = status
        directions = {
            'L': -1,
            'R': 1,
        }
        sa = (sa + directions[op] * value) % 360
        return (sx, sy), sa
    
    def forward(status, op, value):
        (sx, sy), sa = status
        directions = {
            0: (0, -1),
            180: (0, 1),
            90: (1, 0),
            270: (-1, 0),
        }
        dx, dy = directions[sa]
        sx += dx * value
        sy += dy * value
        return (sx, sy), sa


    ops = {
       'N': move,
       'S': move,
       'E': move,
       'W': move,
       'L': rotate,
       'R': rotate,
       'F': forward,
    }

    for line in lines:
        p = parse("{op:l}{value:d}", line)
        if not p:
            printf("Error parsing {line}")
        status = ops[p['op']](status, p['op'], p['value'])

    (sx, sy), sa = status
    print(f'End status: pos:{sx},{sy} angle:{sa} manhattan: {abs(sx) + abs(sy)}')
    print()


def part2(filename):
    print(f"Part 2, reading {filename}")
    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"{len(lines)} read")

    status = (0,0), (10, -1)  # position 0,0, waipoint at 10,-1
    

    def move(status, op, value):
        (sx, sy), (wx, wy) = status
        directions = {
            'N': (0, -1),
            'S': (0, 1),
            'E': (1, 0),
            'W': (-1, 0),
        }
        dx, dy = directions[op]
        wx += dx * value
        wy += dy * value
        return (sx, sy), (wx, wy)
        
    def rotate(status, op, value):
        (sx, sy), (wx, wy) = status
        directions = {
            'L': -1,
            'R': 1,
        }
        angle = (value * directions[op]) % 360
        angles = {
            0: ((sx, sy), (wx, wy)),
            90: ((sx, sy), (-wy, wx)),
            180: ((sx, sy), (-wx, -wy)),
            270: ((sx, sy), (wy, -wx))
        }
        return angles[angle]
    
    def forward(status, op, value):
        (sx, sy), (wx, wy) = status

        sx += wx * value
        sy += wy * value
        return (sx, sy), (wx, wy)


    ops = {
       'N': move,
       'S': move,
       'E': move,
       'W': move,
       'L': rotate,
       'R': rotate,
       'F': forward,
    }

    for line in lines:
        p = parse("{op:l}{value:d}", line)
        if not p:
            printf("Error parsing {line}")
        status = ops[p['op']](status, p['op'], p['value'])
        # (sx, sy), (wx, wy) = status
        # print(f'{line} yields status: pos:{sx},{sy} waypoint:{wx},{wy}')

    (sx, sy), (wx, wy) = status
    print(f'End status: pos:{sx},{sy} waypoint:{wx},{wy} manhattan: {abs(sx) + abs(sy)}')
    print()


def main():
    part1('demo-input')
    part1('input')

    part2('demo-input')
    part2('input')

if __name__ == '__main__':
    main()

# vim: et:ai:sw=4:ts=4
