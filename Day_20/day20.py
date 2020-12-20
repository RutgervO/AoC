#!/usr/bin/env python3

from parse import parse

from itertools import permutations
import math

def calculate(filename, part=1, verbose=False):

    def debug(value):
        if verbose:
            print(value)

    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"\nPart {part}, {filename}, {len(lines)} lines")

    tiles = {}
    tile = []
    for line in lines:
        if line:
            if p:=parse("Tile {tile:d}:", line):
                tiles[p['tile']] = (tile := [])
            else:
                tile.append(line)

    debug(tiles.items())

    tile_size = len(tiles[min(tiles)])
    grid_size = len(tiles)
    dimension = int(math.sqrt(grid_size))  # Assume this always fits :-)
    debug(f"{len(tiles)} tiles, {dimension} x {dimension} grid.")

    def make_number(line):
        return int(line.replace('.', '0').replace('#', '1'), 2)

    sides = {} #  dict title_number -> array of rotations -> array of sides
    all_numbers = {} # tile_number -> set of all side numbers
    for num, tile in tiles.items():
        # store left-to-right, top-to-bottom, as number
        t = make_number(tile[0])
        r = make_number("".join(line[-1] for line in tile))
        b = make_number(tile[-1])
        l = make_number("".join(line[0] for line in tile))
        tr = make_number(tile[0][::-1])
        rr = make_number("".join(line[-1] for line in tile)[::-1])
        br = make_number(tile[-1][::-1])
        lr = make_number("".join(line[0] for line in tile)[::-1])

        numbers = {t, r, b, l, tr, rr, br, lr}
        if len(numbers) != 8:
            print('ERROR - non-unique sides')
            return 0
        all_numbers[num] = numbers

        sides[num] = [
            [ t , r,  b , l  ], # 0 : not rotated
            [ lr, t , rr, b  ], # 1 : rotated 90 cw
            [ br, lr, tr, rr ], # 2 : rotated 180 cw
            [ r , br, l , tr ], # 3 : rotated 270 cw
            
            [ tr, l,  br, r  ], # 4 : flipped horizontally
            [ rr, tr, lr, br ], # 5 : flipped and then rotated 90 cw
            [ b , rr, t , lr ], # 6 : flipped and then rotated 180 cw
            [ l , b , r , t  ], # 7 : flipped and then rotated 270 cw
        ]

    # Solutions are a list of dimenson * dimension tiles
    tile_numbers = tiles.keys()

    # Two ideas:
    # A: all permutations of tiles and check if it can work with rotations
    # B: start with each one of the tiles and see if the grid can be filled in
    # A:
    def solution_A():
        for solution in permutations(tile_numbers, len(tile_numbers)):
            # Check this solution, assume that 4 sides of tile with all rotations are unique
            for rot0 in range(0,8):
                rotations = [rot0]
                for pos in range(1, grid_size):
                    num = solution[pos]
                    nums = sides[num]
                    x = pos % dimension
                    y = pos // dimension
                    rot = -1
                    if x > 0:
                        pr = sides[solution[pos - 1]][rotations[pos - 1]][1]
                        if pr not in all_numbers[num]:
                            break # previous Right does not match anything here
                        for rot in range(8): # There has to be a smart way to immediately find the rotation
                            if nums[rot][3] == pr:
                                break
                        else:
                            break

                    if y > 0:
                        pb = sides[solution[pos - dimension]][rotations[pos - dimension]][2]
                        if pb not in all_numbers[num]:
                            break; # Bottom above does not match anything here
                        if rot >= 0:
                            if nums[rot][0] != pb:
                                break; # Top does not match bottom above at this rotation
                        else:
                            for rot in range(8): # There has to be a smart way to immediately find the rotation
                                if nums[rot][0] == pb:
                                    break
                            else:
                                break
                    if rot < 0:
                        break
                    rotations.append(rot)
                else:
                    debug(f"Solved:\n{solution=}\n{rotations=}")
                    result = solution[0] * solution[dimension - 1] * solution[-dimension] * solution[-1]
                    print(f"Result: {result=}")
                    return result, solution, rotations

    # B:
    def solution_B():
        for start_tile in tile_numbers:
            for rot0 in range(0,8):
                rotations = [rot0]
                solution = [start_tile]
                for pos in range(1, grid_size):
                    x = pos % dimension
                    y = pos // dimension
                    if x > 0:
                        pr = sides[solution[pos - 1]][rotations[pos - 1]][1]
                    if y > 0:
                        pb = sides[solution[pos - dimension]][rotations[pos - dimension]][2]
                    for num in set(tile_numbers) - set(solution):
                        nums = sides[num]
                        rot = -1
                        if x > 0:
                            if pr not in all_numbers[num]:
                                continue  # previous Right does not match anything here
                            for rot in range(8): # There has to be a smart way to immediately find the rotation
                                if nums[rot][3] == pr:
                                    break
                            else:
                                continue

                        if y > 0:
                            if pb not in all_numbers[num]:
                                continue # Bottom above does not match anything here
                            if rot >= 0:
                                if nums[rot][0] != pb:
                                    continue; # Top does not match bottom above at this rotation
                            else:
                                for rot in range(8): # There has to be a smart way to immediately find the rotation
                                    if nums[rot][0] == pb:
                                        break
                                else:
                                    continue
                        if rot < 0:
                            continue

                        solution.append(num)
                        rotations.append(rot)
                        break
                    else:
                        break
                else:
                    debug(f"Solved:\n{solution=}\n{rotations=}")
                    result = solution[0] * solution[dimension - 1] * solution[-dimension] * solution[-1]
                    if part == 1:
                        print(f"Result: {result=}")
                    return result, solution, rotations
                    
    # Solution A is way too slow - solution B is nice and fast

    result, solution, rotations = solution_B()
    if part == 1:
        return result

    def rotate(lines, rot):
        result = lines[:]

        if rot > 3:
            rot -= 4
            result = [_[::-1] for _ in result]

        for i in range(rot):
            result = list("".join(_) for _ in zip(*result[::-1]))

        return result


    picture = []
    new_tile_size = tile_size - 2
    for y in range(dimension):
        for v in range(new_tile_size):
            index = y * new_tile_size + v
            picture.append('')
            for x in range(dimension):
                pos = y * dimension + x
                picture[index] += rotate(tiles[solution[pos]], rotations[pos])[v + 1][1:-1]

    debug('\n'.join(picture))
    
    monster_mask = [
        '                  # ',
        '#    ##    ##    ###',
        ' #  #  #  #  #  #   ',
    ]
    mask_height = len(monster_mask)
    mask_width  = len(monster_mask[0])
    picture_dimension = len(picture)

    def count_a_monster(sx, sy):
        for y in range(mask_height):
            for x in range(mask_width):
                if monster_mask[y][x] == '#':
                    if rot_picture[sy + y][sx + x] != '#':
                        return 0
        return 1

    # Do we only need to find one rotation?? Can monsters overlap?? so much unclear.... ignore any doubt :-)
    for rot in range(8):
        rot_picture = rotate(picture, rot)
        monsters = 0
        for sx in range(picture_dimension - mask_width + 1):
            for sy in range(picture_dimension - mask_height + 1):
                monsters += count_a_monster(sx, sy)
        if monsters:
            count = "".join(rot_picture).count('#') - monsters * "".join(monster_mask).count('#')
            print(f"{monsters} MONSTER(s)! Roughness is {count}")
            return count


def test(value, func, *args, **kwargs):
    result = func(*args, **kwargs)
    if result == value:
        print(f"\nCORRECT! {func.__name__} {args} => {result}")
    else:
        print(f"\nWRONG!   {func.__name__} {args} => {result} but should be {value}")


if __name__ == '__main__':
    test(20899048083289, calculate, 'demo-input', part=1, verbose=False)
    calculate('input', part=1)

    test(273, calculate, 'demo-input', part=2, verbose=False)
    calculate('input', part=2)


# vim: et:ai:sw=4:ts=4
