#!/usr/bin/env python3

from parse import parse
# from collections import namedtuple

def get_nth_number(start_numbers, end_pos, verbose=False):
    def debug(value):
        if verbose:
            print(value)

    numbers = start_numbers[:]

    print(f"\nPart 1, {numbers}, find number on position {end_pos}.")

    last_index = {}
    number = 0
    for p in range(0, end_pos):
        if p < len(start_numbers):
            number = numbers[p]
            last_index[number] = p
        else:
            number = p - 1 - last_index.get(last_num, p - 1)
            last_index[last_num] = p-1

            debug(f"{p=} {last_num=} {number=}")

        last_num = number

    result = number
    print(f'Result: {result}')
    return result


def test(value, func, *args, **kwargs):
    result = func(*args, **kwargs)
    if result == value:
        print("CORRECT!")
    else:
        print(f"WRONG! Result should be {value} but {result} was found.")


def main():
    test(436, get_nth_number, [0, 3, 6], 2020)
    test(1, get_nth_number, [1, 3, 2], 2020)
    test(10, get_nth_number, [2, 1, 3], 2020)
    test(27, get_nth_number, [1, 2, 3], 2020)
    test(78, get_nth_number, [2, 3, 1], 2020)
    test(438, get_nth_number, [3, 2, 1], 2020)
    test(1836, get_nth_number, [3, 1, 2], 2020)

    get_nth_number([8,13,1,0,18,9], 2020)

    test(175594, get_nth_number, [0, 3, 6], 30000000)
    test(2578, get_nth_number, [1, 3, 2], 30000000)
    test(3544142, get_nth_number, [2, 1, 3], 30000000)
    test(261214, get_nth_number, [1, 2, 3], 30000000)
    test(6895259, get_nth_number, [2, 3, 1], 30000000)
    test(18, get_nth_number, [3, 2, 1], 30000000)
    test(362, get_nth_number, [3, 1, 2], 30000000)

    get_nth_number([8,13,1,0,18,9], 30000000)

if __name__ == '__main__':
    main()

# vim: et:ai:sw=4:ts=4
