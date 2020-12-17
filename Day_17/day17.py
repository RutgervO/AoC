#!/usr/bin/env python3

from itertools import product


def calculate_it(filename, dimensions, steps=6, verbose=False):

    def debug(value):
        if verbose:
            print(value)


    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"\n{filename}, {dimensions} dimensions, {steps} steps, {len(lines)} lines")

    neighbours = list(product([-1, 0, 1], repeat=dimensions))
    zero_coord = tuple([0] * dimensions)
    neighbours.remove(zero_coord)

    state = dict()  # Coord -> int
    for y, line in enumerate(lines):
        for x, value in enumerate(line):
            if value == '#':
                coord = [0] * dimensions    # TODO
                coord[0] = x
                coord[1] = y
                state[tuple(coord)] = 1
            
    debug(f"State contains {len(state)} activate cubes.")


    def count_neighbours(state, coord, neighbours):
        return sum([state.get(tuple(map(sum, zip(coord, neighbour))), 0)
                    for neighbour in neighbours])


    def cube_plus_one(*args): # argument: tuples of range, one for each dimension.
        return list(product(*map(lambda x: range(x[0] - 1, x[1] + 2), args)))


    for step in range(0, steps):

        new_state = dict()

        # rule 1, and keep track of limits
        smallest = zero_coord
        largest = zero_coord

        for coord, value in state.items():
            count = count_neighbours(state, coord, neighbours)

            if value == 1 and count in {2,3}:
                new_state[coord] = 1
            
            smallest = tuple(map(min, zip(coord, smallest)))
            largest = tuple(map(max, zip(coord, largest)))
        
        # rule 2
        for coord in cube_plus_one(*zip(smallest, largest)):
            if state.get(coord, 0) == 0:
                if count_neighbours(state, coord, neighbours) == 3:
                    new_state[coord] = 1

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
    test(112, calculate_it, 'demo-input', 3)
    calculate_it('input', 3)

    test(848, calculate_it, 'demo-input', 4)
    calculate_it('input', 4)


if __name__ == '__main__':
    main()

# vim: et:ai:sw=4:ts=4
