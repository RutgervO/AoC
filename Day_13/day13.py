#!/usr/bin/env python3

# from parse import *
# from collections import namedtuple

from math import ceil, lcm


def part1(filename):
    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"Part 1, {filename}, {len(lines)} lines")

    arrival = int(lines[0])

    busses = [int(busline) for busline in lines[1].split(',') if busline != 'x']

    print(f"Arrival timestamp: {arrival}")
    print(f"Busses: {busses}")

    earliest_bus = None
    earliest_time = 0
    for busline in busses:
        next_arrival = ceil(arrival / busline) * busline
        if not earliest_bus or next_arrival < earliest_time:
            earliest_bus = busline
            earliest_time = next_arrival

    print(f"The first bus to arrive is {earliest_bus} at {earliest_time}")
    print(f"Answer: {(earliest_time - arrival) * earliest_bus}\n")


def part2_brute(filename):
    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"Part 2 BRUTE FORCE, {filename}, {len(lines)} lines")

    values = lines[1].split(',')
    busses = [int(value) for value in values if value != 'x']
    offset = [count for count, value in enumerate(values) if value != 'x']
    len_busses = len(busses)
        
    print(f"Busses: {busses}")
    print(f"Offset: {offset}")

    # Brute Force
    i = 0
    while True:
        t = busses[0] * i
        for j in range(1, len_busses):
            if ((t + offset[j]) / busses[j]) % 1 != 0:
                break
        else:
            print(f"Found timestamp {t}")
            return t
        i += 1
    

def part2_brute2(filename, start = 0):
    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"Part 2 smarter brute force, {filename}, {len(lines)} lines")

    values = lines[1].split(',')
    busses = [int(value) for value in values if value != 'x']
    offset = [count for count, value in enumerate(values) if value != 'x']
    len_busses = len(busses)
        
    print(f"Busses: {busses}")
    print(f"Offset: {offset}")

    # Brute Force - at least use the biggest bus
    bbus = -1
    bbus_offset = 0
    for index, value in enumerate(busses):
        if value > bbus:
            bbus = value
            bbus_offset = offset[index]
    
    i = 0
    i = start // bbus # CHEATING :-)

    while True:
        t = bbus * i - bbus_offset

        if i % 10000000 == 0:
            print(f"Processed {i}, current timestamp {t}")
        
        for j in range(0, len_busses):
            if ((t + offset[j]) / busses[j]) % 1 != 0:
                break
        else:
            print(f"Found timestamp {t}")
            return t
        i += 1


def part2_chinese_wrong(filename, start = 0):
    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"Part 2 chinese remainder, {filename}, {len(lines)} lines")

    values = lines[1].split(',')
    busses = [int(value) for value in values if value != 'x']
    offset = [count for count, value in enumerate(values) if value != 'x']
    len_busses = len(busses)
        
    print(f"Busses: {busses}")
    print(f"Offset: {offset}")


    # chinese remainder problem? different modulos(buslines) and remainders(intervals)
    # t mod b0 == 0
    # (t + i1) mod b1 == 0
    # (t + i2) mod b2 == 0

    # t mod b0 = 0
    # (t + i1) mod b1 = 0  =>  t mod b1 = i1 mod b1
    # (t + i2) mod b2 = 0  =>  t mod b2 = i2 mod b2

    remainders = []
    for index, bus in enumerate(busses):
        remainder = offset[index] % bus
        remainders.append(remainder)
        print(f"t mod {bus} = {remainder}")

    print(f"Remainders: {remainders}")

    # Solved via https://www.dcode.fr/chinese-remainder ... pfff
    # How can I do this myself? No clue...
    # Code from: https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6

    from functools import reduce
    def chinese_remainder(n, a):
        sum = 0
        prod = reduce(lambda a, b: a*b, n)
        for n_i, a_i in zip(n, a):
            p = prod // n_i
            sum += a_i * mul_inv(p, n_i) * p
        return sum % prod

    def mul_inv(a, b):
        b0 = b
        x0, x1 = 0, 1
        if b == 1: return 1
        while a > 1:
            q = a // b
            a, b = b, a%b
            x0, x1 = x1 - q * x0, x0
        if x1 < 0: x1 += b0
        return x1

    result = chinese_remainder(busses, remainders)
    print(f"Result: {result}")
    return result
    

def part2_sorted_brute(filename, start = 0):
    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"Part 2 sorted brute force, {filename}, {len(lines)} lines")

    values = lines[1].split(',')
    busses = [int(value) for value in values if value != 'x']
    offset = [count for count, value in enumerate(values) if value != 'x']
    len_busses = len(busses)
        
    print(f"Busses: {busses}")
    print(f"Offset: {offset}")

    # sort busses and offsets
    sbusses = busses[:]
    sbusses.sort(reverse=True)
    soffset = [offset[busses.index(bus)] for bus in sbusses]

    print(f"Sorted Busses: {sbusses}")
    print(f"Sorted Offset: {soffset}")

    busses = sbusses[:]
    offset = soffset[:]

    i = start // busses[0] # CHEATING :-)

    while True:
        t = busses[0] * i - offset[0]

        if i % 10000000 == 0:
            print(f"Processed {i}, current timestamp {t}")
        
        for j in range(0, len_busses):
            if ((t + offset[j]) / busses[j]) % 1 != 0:
                break
        else:
            print(f"Found timestamp {t}")
            return t
        i += 1


def part2(filename, start = 0):
    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"Part 2 sorted multipying increments, {filename}, {len(lines)} lines")

    values = lines[1].split(',')
    busses = [int(value) for value in values if value != 'x']
    offset = [count for count, value in enumerate(values) if value != 'x']
    len_busses = len(busses)
        
    print(f"Busses: {busses}")
    print(f"Offset: {offset}")

    # sort busses and offsets
    sbusses = busses[:]
    sbusses.sort(reverse=True)
    soffset = [offset[busses.index(bus)] for bus in sbusses]

    print(f"Sorted Busses: {sbusses}")
    print(f"Sorted Offset: {soffset}")

    busses = sbusses[:]
    offset = soffset[:]

    increment = 1
    t = -increment
    correct_busses = 0

    while True:
        t += increment
        for j in range(correct_busses, len_busses):
            if ((t + offset[j]) / busses[j]) % 1 != 0:
                break
            else:
                correct_busses += 1
                increment *= busses[j]
        else:
            print(f"Found timestamp {t}")
            return t


def test(func, filename, value):
    result = func(filename)
    if result == value:
        print("CORRECT!\n")
    else:
        print(f"WRONG! Result should be {value} but {result} was found.\n")


def main():
    part1('demo-input')
    part1('input')

    test(part2, 'demo-input', 1068781)
    test(part2, 'demo-input-part2-1', 754018)
    test(part2, 'demo-input-part2-2', 779210)
    test(part2, 'demo-input-part2-3', 1261476)
    test(part2, 'demo-input-part2-4', 1202161486)
    part2('input', 100000000000000)


if __name__ == '__main__':
    main()

# vim: et:ai:sw=4:ts=4
