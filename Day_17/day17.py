#!/usr/bin/env python3

from collections import defaultdict, namedtuple


def part1(filename, verbose=False):

    def debug(value):
        if verbose:
            print(value)

    Coord = namedtuple('Coordinate', 'x y z')

    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"\nPart 1 {filename}, {len(lines)} lines")

    state = dict()  # Coord -> int
    z = 0
    for y, line in enumerate(lines):
        for x, value in enumerate(line):
            if value == '#':
                state[Coord(x, y, z)] = 1
            
    debug(f"State contains {len(state)} activate cubes.")

    def count_neighbours(state, coord):
        neighbours = [
            (-1, -1, -1), (-1, -1,  0), (-1, -1,  1),
            (-1,  0, -1), (-1,  0,  0), (-1,  0,  1),
            (-1,  1, -1), (-1,  1,  0), (-1,  1,  1),
            ( 0, -1, -1), ( 0, -1,  0), ( 0, -1,  1),
            ( 0,  0, -1),               ( 0,  0,  1),
            ( 0,  1, -1), ( 0,  1,  0), ( 0,  1,  1),
            ( 1, -1, -1), ( 1, -1,  0), ( 1, -1,  1),
            ( 1,  0, -1), ( 1,  0,  0), ( 1,  0,  1),
            ( 1,  1, -1), ( 1,  1,  0), ( 1,  1,  1),
        ]
        result = 0
        for dx, dy, dz in neighbours:
            result += state.get(Coord(coord.x + dx, coord.y + dy, coord.z + dz), 0)
        return result


    for step in range(0, 6):

        new_state = dict()

        # rule 1, and keep track of limits
        smallest = Coord(0, 0, 0)
        largest = Coord(0, 0, 0)

        #items = list(state.items())
        #debug(items)
        for coord, value in state.items():
            neighbours = count_neighbours(state, coord)

            if value == 1 and neighbours in {2,3}:
                new_state[coord] = 1
            
            smallest = Coord(min(smallest.x, coord.x),
                             min(smallest.y, coord.y),
                             min(smallest.z, coord.z))
            largest  = Coord(max(largest.x, coord.x),
                             max(largest.y, coord.y),
                             max(largest.z, coord.z))
        
        # rule 2
        for x in range(smallest.x - 1, largest.x + 2):
            for y in range(smallest.y - 1, largest.y + 2):
                for z in range(smallest.z - 1, largest.z + 2):
                    coord = Coord(x, y, z)
                    if state.get(coord, 0) == 0:
                        if count_neighbours(state, coord) == 3:
                            new_state[coord] = 1

        # DEBUG!
        if verbose:
            for z in range(smallest.z - 1, largest.z + 2):
                debug(f"{z=}")
                for y in range(smallest.y - 1, largest.y + 2):
                    debug("".join(".#"[new_state.get(Coord(x, y, z), 0)]
                                       for x in range(smallest.x - 1, largest.x + 2)))

        state = new_state
        debug(f"After step {step + 1} State contains {len(state)} activate cubes.")

    result = len(state) 
    print(f'Result: {result}')
    return result


def part2(filename, verbose=False):

    def debug(value):
        if verbose:
            print(value)

    Coord = namedtuple('Coordinate', 'x y z w')

    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"\nPart 2 {filename}, {len(lines)} lines")

    state = dict()  # Coord -> int
    w, z = 0, 0
    for y, line in enumerate(lines):
        for x, value in enumerate(line):
            if value == '#':
                state[Coord(x, y, z, w)] = 1
            
    debug(f"State contains {len(state)} activate cubes.")

    def count_neighbours(state, coord):
        neighbours = [
            (-1, -1, -1, -1), (-1, -1,  0, -1), (-1, -1,  1, -1),
            (-1,  0, -1, -1), (-1,  0,  0, -1), (-1,  0,  1, -1),
            (-1,  1, -1, -1), (-1,  1,  0, -1), (-1,  1,  1, -1),
            ( 0, -1, -1, -1), ( 0, -1,  0, -1), ( 0, -1,  1, -1),
            ( 0,  0, -1, -1), ( 0,  0,  0, -1), ( 0,  0,  1, -1),
            ( 0,  1, -1, -1), ( 0,  1,  0, -1), ( 0,  1,  1, -1),
            ( 1, -1, -1, -1), ( 1, -1,  0, -1), ( 1, -1,  1, -1),
            ( 1,  0, -1, -1), ( 1,  0,  0, -1), ( 1,  0,  1, -1),
            ( 1,  1, -1, -1), ( 1,  1,  0, -1), ( 1,  1,  1, -1),

            (-1, -1, -1,  0), (-1, -1,  0,  0), (-1, -1,  1,  0),
            (-1,  0, -1,  0), (-1,  0,  0,  0), (-1,  0,  1,  0),
            (-1,  1, -1,  0), (-1,  1,  0,  0), (-1,  1,  1,  0),
            ( 0, -1, -1,  0), ( 0, -1,  0,  0), ( 0, -1,  1,  0),
            ( 0,  0, -1,  0),                   ( 0,  0,  1,  0),
            ( 0,  1, -1,  0), ( 0,  1,  0,  0), ( 0,  1,  1,  0),
            ( 1, -1, -1,  0), ( 1, -1,  0,  0), ( 1, -1,  1,  0),
            ( 1,  0, -1,  0), ( 1,  0,  0,  0), ( 1,  0,  1,  0),
            ( 1,  1, -1,  0), ( 1,  1,  0,  0), ( 1,  1,  1,  0),

            (-1, -1, -1,  1), (-1, -1,  0,  1), (-1, -1,  1,  1),
            (-1,  0, -1,  1), (-1,  0,  0,  1), (-1,  0,  1,  1),
            (-1,  1, -1,  1), (-1,  1,  0,  1), (-1,  1,  1,  1),
            ( 0, -1, -1,  1), ( 0, -1,  0,  1), ( 0, -1,  1,  1),
            ( 0,  0, -1,  1), ( 0,  0,  0,  1), ( 0,  0,  1,  1),
            ( 0,  1, -1,  1), ( 0,  1,  0,  1), ( 0,  1,  1,  1),
            ( 1, -1, -1,  1), ( 1, -1,  0,  1), ( 1, -1,  1,  1),
            ( 1,  0, -1,  1), ( 1,  0,  0,  1), ( 1,  0,  1,  1),
            ( 1,  1, -1,  1), ( 1,  1,  0,  1), ( 1,  1,  1,  1),
        ]
        result = 0
        for dx, dy, dz, dw in neighbours:
            result += state.get(Coord(coord.x + dx, coord.y + dy, coord.z + dz, coord.w + dw), 0)
        return result


    for step in range(0, 6):

        new_state = dict()

        # rule 1, and keep track of limits
        smallest = Coord(0, 0, 0, 0)
        largest = Coord(0, 0, 0, 0)

        for coord, value in state.items():
            neighbours = count_neighbours(state, coord)

            if value == 1 and neighbours in {2,3}:
                new_state[coord] = 1
            
            smallest = Coord(min(smallest.x, coord.x),
                             min(smallest.y, coord.y),
                             min(smallest.z, coord.z),
                             min(smallest.w, coord.w))
            largest  = Coord(max(largest.x, coord.x),
                             max(largest.y, coord.y),
                             max(largest.z, coord.z),
                             max(largest.w, coord.w))
        
        # rule 2
        for x in range(smallest.x - 1, largest.x + 2):
            for y in range(smallest.y - 1, largest.y + 2):
                for z in range(smallest.z - 1, largest.z + 2):
                    for w in range(smallest.w - 1, largest.w + 2):
                        coord = Coord(x, y, z, w)
                        if state.get(coord, 0) == 0:
                            if count_neighbours(state, coord) == 3:
                                new_state[coord] = 1

        # DEBUG!
        if verbose:
            for w in range(smallest.w - 1, largest.w + 2):
                for z in range(smallest.z - 1, largest.z + 2):
                    debug(f"{z=}, {w=}")
                    for y in range(smallest.y - 1, largest.y + 2):
                        debug("".join(".#"[new_state.get(Coord(x, y, z, w), 0)]
                                           for x in range(smallest.x - 1, largest.x + 2)))

        state = new_state
        debug(f"After step {step + 1} State contains {len(state)} activate cubes.")

    result = len(state) 
    print(f'Result: {result}')
    return result

def test(value, func, *args, **kwargs):
    result = func(*args, **kwargs)
    if result == value:
        print("CORRECT!")
    else:
        print(f"WRONG! Result should be {value} but {result} was found.")


def main():
    test(112, part1, 'demo-input')
    part1('input')

    test(848, part2, 'demo-input')
    part2('input')


if __name__ == '__main__':
    main()

# vim: et:ai:sw=4:ts=4
