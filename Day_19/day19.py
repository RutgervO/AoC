#!/usr/bin/env python3

from functools import cache
import re

def calculate(filename, part=1, verbose=False):

    def debug(value):
        if verbose:
            print(value)

    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"\nPart {part}, {filename}, {len(lines)} lines")

    rules = {}
    messages = []

    for line in lines:
        if ':' in line:
            number = int(line.split(':')[0])
            rest = line.split(':')[1].strip()
            rule = {
                'literal': None,
                'nexts': [],
            }
            if '"' in line:
                rule['literal'] = rest[1]
            elif '|' in line:
                rule['next'] = [[int(_) for _ in split.strip().split(' ')] for split in rest.split('|')]
            else:
                rule['next'] = [[int(_) for _ in rest.split(' ')]]
            rules[number] = rule
        else:
            if len(line):
                messages.append(line)

    print(f"{len(rules)} rules, {len(messages)} messages")

    @cache
    def build_regex(num, part):
        rule = rules[num]
        if literal := rule['literal']:
            return literal
        if part == 2:
            if num == 8:
                return f"(?:{build_regex(42, part)}+)"
            if num == 11:
                left = build_regex(42, part)
                right = build_regex(31, part)
                # Aaargh python regex module does not support balanced constructs
                # Do it the Jarmo way!
                return f"(?:" + "|".join([f"{left}{{{i}}}{right}{{{i}}}" for i in range(1, 100)]) + ")"
        return "(?:" + \
                "|".join(["".join([build_regex(subnum, part) for subnum in sublist]) for sublist in rule['next']]) + \
                ")"
        
    regex = re.compile(build_regex(0, part))

    result = 0
    for message in messages:
        debug(f"{message}")
        if regex.fullmatch(message):
            debug(f"{message} parses")
            result += 1

    print(f'Result: {result}')
    return result


def test(value, func, *args, **kwargs):
    result = func(*args, **kwargs)
    if result == value:
        print(f"\nCORRECT! {func.__name__} {args} => {result}")
    else:
        print(f"\nWRONG!   {func.__name__} {args} => {result} but should be {value}")


if __name__ == '__main__':
    test(2, calculate, 'demo-input', part=1, verbose=False)
    calculate('input', part=1)

    calculate('input', part=2)


# vim: et:ai:sw=4:ts=4
