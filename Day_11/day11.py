#!/usr/bin/env python3
"""
All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:

    If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    Otherwise, the seat's state does not change.

Floor (.) never changes; seats don't move, and nobody sits on the floor.
"""

def part1(filename):
    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]
    print(f"{len(lines)} lines read from {filename}")
    grid = lines[:]

    def how_many_adjacent_occupied(grid, x, y):
        rows = len(grid)
        cols = len(grid[0])
        
        count = 0
        checks = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        for cx, cy in checks:
            cx += x
            cy += y
            if (0 <= cx < cols) and (0 <= cy < rows):
                count += grid[cy][cx] == '#'

        return count

    def apply_rules(old_grid):
        rows = len(old_grid)
        cols = len(old_grid[0])
        
        new_grid = []
        for y in range(0, rows):
            new_grid.append("")
            for x in range(0, cols):
                old = old_grid[y][x]
                new = old
                if old != '.':
                    adjacent = how_many_adjacent_occupied(old_grid, x, y)
                    if old == 'L' and adjacent == 0:
                        new = '#'
                    elif old == '#' and adjacent >= 4:
                        new = 'L'
                new_grid[y] += new
        return new_grid

    step = 0
    while True:
        lf = '\n'
        print(f"Step {step} occupied seats: {str(grid).count('#')}\n{lf.join(grid)}\n")
        step += 1
        new_grid = apply_rules(grid)
        if str(new_grid) == str(grid):
            print("Stable!")
            return
        grid = new_grid[:]


def part2(filename):
    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]
    print(f"{len(lines)} lines read from {filename}")
    grid = lines[:]

    def how_many_visible_occupied(grid, x, y):
        rows = len(grid)
        cols = len(grid[0])
        
        count = 0
        checks = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        for dx, dy in checks:
            cx = x
            cy = y
            while True:
                cx += dx
                cy += dy
                if (0 <= cx < cols) and (0 <= cy < rows):
                    place = grid[cy][cx]
                    if place == '#':
                        count += 1
                        break
                    if place == 'L':
                        break
                else:
                    break

        return count

    def apply_rules(old_grid):
        rows = len(old_grid)
        cols = len(old_grid[0])
        
        new_grid = []
        for y in range(0, rows):
            new_grid.append("")
            for x in range(0, cols):
                old = old_grid[y][x]
                new = old
                if old != '.':
                    adjacent = how_many_visible_occupied(old_grid, x, y)
                    if old == 'L' and adjacent == 0:
                        new = '#'
                    elif old == '#' and adjacent >= 5:
                        new = 'L'
                new_grid[y] += new
        return new_grid

    step = 0
    while True:
        lf = '\n'
        print(f"Step {step} occupied seats: {str(grid).count('#')}\n{lf.join(grid)}\n")
        step += 1
        new_grid = apply_rules(grid)
        if str(new_grid) == str(grid):
            print("Stable!")
            return
        grid = new_grid[:]
if __name__ == '__main__':
    print('Part 1 - demo')
    part1('input_demo_1')

    print('Part 1 - real')
    part1('input')

    print('Part 2 - demo')
    part2('input_demo_1')

    print('Part 2 - real')
    part2('input')

# vim: ai:sw=4:ts=4:et
