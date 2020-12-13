#!/usr/bin/env python3

from math import ceil


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
