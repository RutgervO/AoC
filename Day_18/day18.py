#!/usr/bin/env python3

from parse import parse
# from collections import namedtuple


def calculate(string, part, verbose=False):

    def debug(value):
        if verbose:
            print(value)

    debug(string)
    strings = string.replace('(', '( ').replace(')', ' )').split()

    # calculate any sub parts

    while '(' in strings:
        pos = strings.index('(')
        # find the matching ')'
        counts = {'(': 1, ')': -1}
        count = 1
        for endpos in range(pos + 1, len(strings)):
            count += counts.get(strings[endpos], 0)
            if not count:
                break
        else:
            print("error: no matching ')' found")
            return None
        strings = strings[ : pos] + [str(calculate(" ".join(strings[pos+1 : endpos]), part, verbose))] + strings[endpos + 1 : ]

    debug(f"No parenthesis: {strings}")

    # Now we only have numbers and operators
    if part == 2:

        # PART 2: Do the additions first

        while '+' in strings:
            pos = strings.index('+')
            total = int(strings[pos - 1]) + int(strings[pos + 1])
            strings = strings [ : pos - 1] + [str(total)] + strings[pos + 2 : ]

    # Now we only have numbers and operators, calculate left to right

    total = int(strings[0])
    for pos in range(1, len(strings), 2):
        operator = strings[pos]
        num = int(strings[pos + 1])
        if operator == '+':
            total += num
        elif operator == '*':
            total *= num
        else:
            print(f"Invalid operator {operator}")
            return None

    return total


def calculate_sum(filename, part, verbose=False):

    def debug(value):
        if verbose:
            print(value)


    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"\nPart {part}, {filename}, {len(lines)} lines")

    result = 0
    for line in lines:
        result += calculate(line, part, verbose)

    print(f'Result: {result}')
    return result


def test(value, func, *args, **kwargs):
    result = func(*args, **kwargs)
    if result == value:
        print(f"\nCORRECT! {func.__name__} {args} => {result}")
    else:
        print(f"\nWRONG!   {func.__name__} {args} => {result} but should be {value}")


def main():
    tests = [('1 + 2 * 3 + 4 * 5 + 6', 71),
             ('2 * 3 + (4 * 5) ', 26),
             ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 437),
             ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 12240),
             ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632),
            ]
    for string, result in tests:
        test(result, calculate, string, 1)

    calculate_sum('input', 1)

    tests = [('1 + (2 * 3) + (4 * (5 + 6))', 51),
             ('2 * 3 + (4 * 5)',  46),
             ('5 + (8 * 3 + 9 + 3 * 4 * 3)', 1445),
             ('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 669060),
             ('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 23340),
            ]

    for string, result in tests:
        test(result, calculate, string, 2)

    calculate_sum('input', 2)

if __name__ == '__main__':
    main()

# vim: et:ai:sw=4:ts=4
