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

    all_valid_numbers = set()
    all_invalid_numbers = []

    phase = 0 # [rules, your ticket, nearby tickets]
    phases = {'your ticket': 1, 'nearby tickets': 2}
    

    for line in lines:
        if line != '':

            if line[-1] == ':':
                phase = phases.get(line[:-1], phase)

            elif phase == 0:
                p = parse("{field}: {v1:d}-{v2:d} or {v3:d}-{v4:d}", line)
                
                all_valid_numbers.update(range(p['v1'], p['v2'] + 1))
                all_valid_numbers.update(range(p['v3'], p['v4'] + 1))

            elif phase == 1:
                continue

            elif phase == 2:
                numbers = [int(_) for _ in line.split(',')]
                invalid_numbers = set(numbers) 
                invalid_numbers -= all_valid_numbers

                all_invalid_numbers.extend(invalid_numbers)

            else:
                print("Error!")
                return 0

    result = sum(all_invalid_numbers)
    print(f'Result: {result}')
    return result


def part2(filename, verbose=True):

    def debug(value):
        if verbose:
            print(value)

    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"\nPart 2, {filename}, {len(lines)} lines")

    all_valid_numbers = set()
    your_ticket = []
    valid_nearby_tickets = []
    rules = {}

    phase = 0 # 0 = rules
    phases = {'your ticket': 1, 'nearby tickets': 2}

    for line in lines:
        if line != '':

            if line[-1] == ':':
                phase = phases.get(line[:-1], phase)

            elif phase == 0:
                p = parse("{field}: {v1:d}-{v2:d} or {v3:d}-{v4:d}", line)
                
                numbers = set(range(p['v1'], p['v2'] + 1)) | \
                          set(range(p['v3'], p['v4'] + 1))
                        
                all_valid_numbers.update(numbers)
                rules[p["field"]] = numbers

            elif phase == 1:
                your_ticket = [int(_) for _ in line.split(',')]

            elif phase == 2:
                ticket = [int(_) for _ in line.split(',')]
                invalid_numbers = set(ticket) - all_valid_numbers
                if not invalid_numbers:
                    valid_nearby_tickets.append(ticket)

            else:
                print("Error!")
                return 0

    # In the beginning, anything is possible!
    possibles = []
    fields = rules.keys()  # ordered dict by default, woo!
    for field in fields:
        possibles.append(set(fields))
    
    # Check all the fields for each valid nearby ticket
    for ticket in valid_nearby_tickets:
        for index, value in enumerate(ticket):
            invalids = set()
            for rule in possibles[index]:
                if value not in rules[rule]:
                    invalids.add(rule)
            if invalids:
                possibles[index] -= invalids

    # Eliminate singles from fields with mutiple possibilities - until done, or for eternity
    singles = set()
    while len(singles) < len(possibles):
        for possible in possibles:
            if len(possible) == 1:
                singles.add(min(possible))
            elif len(possible) > 1:
                possible -= singles
            else:
                print("Error - no possible solution!")
                return 0

    print("Fields:")
    result = 1
    for index, possible in enumerate(possibles):
        field = min(possible)
        value = your_ticket[index]
        if field.startswith("departure"):
            result *= value
            value = f"{value} *"

        print(f"{index:2d} {field:20s} {value}")
    
    print(f'Result: {result}')
    return result


def test(func, filename, value):
    result = func(filename)
    if result == value:
        print("CORRECT!")
    else:
        print(f"WRONG! Result should be {value} but {result} was found.")


def main():
    test(part1, 'demo-input', 71)
    part1('input')

    part2('demo-input')
    part2('input')


if __name__ == '__main__':
    main()

# vim: et:ai:sw=4:ts=4
