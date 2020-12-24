#!/usr/bin/env python3

from collections import defaultdict


class Tile:
    color, x, y = 0, 0, 0   # 0 = White
    grid = None
    moves = ['e', 'se', 'sw', 'w', 'nw', 'ne']
    directions =  [(2, 0), (1, 1), (-1, 1), (-2, 0), (-1, -1), (1, -1)]

    def __init__(self, grid, x, y):
        self.grid = grid
        self.x = x
        self.y = y

    def process(self, line):
        if not len(line):
            self.color = 1 - self.color
        else:
            for index, direction in enumerate(self.moves):
                if line.startswith(direction):
                    dx, dy = self.directions[index]
                    x, y = self.x + dx, self.y + dy
                    neighbour = self.grid.get((x, y), Tile(self.grid, x, y))
                    self.grid[(x,y)] = neighbour
                    neighbour.process(line[len(direction):])

    def count_color(self, color):
        count = 0
        for tile in self.grid.values():
            if tile.color == color:
                count += 1
        return count

    def count_neighbours_of_color(self, color):
        count = 0
        for dx, dy in self.directions:
            x, y = self.x + dx, self.y + dy
            if (tile := self.grid.get((x, y), None)):
                if tile.color == color:
                    count += 1
        return count
        
    def spread(self):
        # Surround any black tiles on the grid with white ones
        for tile in list(self.grid.values()):
            if tile.color == 1:
                for dx, dy in self.directions:
                    x, y = tile.x + dx, tile.y + dy
                    neighbour = self.grid.get((x, y), Tile(self.grid, x, y))
                    self.grid[(x,y)] = neighbour


    def __repr__(self):
        return f'({self.x},{self.y})=' + str(self)

    def __str__(self):
        return ["WT", "BT"][self.color]
    
    def print_grid(self):
        sx = ex = sy = ey = 0
        for tile in self.grid.values():
            sx = min(sx, tile.x)
            ex = max(ex, tile.x)
            sy = min(sy, tile.y)
            ey = max(ey, tile.y)
        print(f"Grid {sx},{sy} - {ex},{ey}:")
        for y in range(sy, ey + 1):
            print(f"{y:3d} ", end='')
            if y % 2:
                print(' ', end='')
            for x in range(sx, ex + 1):
                if (y % 2) == (x % 2):
                    tile = self.grid.get((x, y), None)
                    if tile:
                        print(tile, end='')
                    else:
                        print('  ', end='')
            print()

def calculate(filename, part=1, verbose=False):

    def debug(value):
        if verbose:
            print(value)

    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"\nPart {part}, {filename}, {len(lines)} lines")

    grid = {}
    grid[(0,0)] = startTile = Tile(grid, 0, 0)
    for line in lines:
        startTile.process(line)

    if part == 2:
        for day in range(1, 101):
            startTile.spread()

            rule1 = set()
            rule2 = set()

            for tile in grid.values():
                count = tile.count_neighbours_of_color(1)

                if tile.color == 1: # Rule1: black tiles with 0 or >2 black neighbours => white
                    if count == 0 or count > 2:
                        rule1.add(tile)
                else: # Rule2: white tiles with 2 black neighbours => black
                    if count == 2:
                        rule2.add(tile)

            for tile in rule1:
                tile.color = 0

            for tile in rule2:
                tile.color = 1
                
            result = startTile.count_color(1)

            if verbose:
                startTile.print_grid()
            debug(f"Day {day}: {result}")

    result = startTile.count_color(1)

    print(f'{result} tiles are block.')
    return result
    

if __name__ == '__main__':
    assert(calculate('demo-input', part=1, verbose=False) == 10)
    assert(calculate('input', part=1, verbose=False) == 436)

    assert(calculate('demo-input', part=2, verbose=False) == 2208)
    assert(calculate('input', part=2, verbose=False) == 4133)


# vim: et:ai:sw=4:ts=4
