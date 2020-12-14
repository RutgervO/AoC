#!/usr/bin/env python3

from parse import parse
# from collections import namedtuple

def part1(filename, verbose=False):
    def debug(value):
        if verbose:
            print(value)


    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"\nPart 1, {filename}, {len(lines)} lines")

    mask0 = 0
    mask1 = 0
    mem = {}
    for line in lines:
        debug(f"Step: {line}")
        if p:=parse("mask = {mask:36w}", line):
            mask = p['mask']
            mask1 = int(mask.replace('X', '0'), 2)
            mask0 = int(mask.replace('X', '1'), 2)

            debug(f"{mask=}\n{mask0=:036b}\n{mask1=:036b}")

        elif p:=parse("mem[{address:d}] = {value:d}", line):
            address = p['address']
            value = p['value']
            value = (value | mask1) & mask0
            mem[address] = value

            debug(f"{address=}\n{value=:036b}")

        else:   
            print("ERROR")
            return 0

    total = sum(mem.values())
    print(f'Total: {total}')
    return total


def part2(filename, verbose=False):

    def debug(value):
        if verbose:
            print(value)

    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"\nPart 2, {filename}, {len(lines)} lines")

    mask1 = 0
    maskx = 0
    countx = 0
    xpos = []
    mem = {}
    for line in lines:

        debug(f"Step: {line}")

        if p:=parse("mask = {mask:36w}", line):
            mask = p['mask']
            mask1 = int(mask.replace('X', '0'), 2)
            maskx = int(mask.replace('1', '0').replace('X', '1'), 2)

            v = 1
            xpos = []
            for i in range(0, 36):
                if maskx & v:
                    xpos.append(v)
                v <<= 1
            countx = len(xpos)
            
            debug(f"{mask=}\n{mask1=:036b}\n{maskx=:036b}\n{xpos=}")

        elif p:=parse("mem[{address:d}] = {value:d}", line):
            address = p['address']
            value = p['value']

            debug(f"{address=:036b}")

            address |= mask1
            address &= maskx ^ (2 ** 36 -1)

            debug(f"{address=:036b}")

            for i in range(0, 2 ** countx):
                floating = 0
                for source, dest in enumerate(xpos):
                    if i & (2 ** source):
                        floating |= dest

                debug(f"Floating: {floating:036b} => {address | floating:036b}")

                mem[address | floating] = value
        else:   
            print("ERROR")
            return 0

    total = sum(mem.values())
    print(f'Total: {total}')
    return total


def test(value, func, *args, **kwargs):
    result = func(*args, **kwargs)
    if result == value:
        print("CORRECT!")
    else:
        print(f"WRONG! Result should be {value} but {result} was found.")


def main():
    test(165, part1, 'demo-input', True)
    part1('input')

    test(208, part2, 'demo-input-2', True)
    part2('input')


if __name__ == '__main__':
    main()

# vim: et:ai:sw=4:ts=4
