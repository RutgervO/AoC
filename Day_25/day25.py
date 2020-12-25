#!/usr/bin/env python3

initial_subject = 7
modulus = 20201227


def get_loop_sizes(keys, subject = initial_subject):
    value = 1
    found = 0
    loop = 0
    result = [None, None]
    while found != 2:
        if value in keys:
            result[keys.index(value)] = loop
            found += 1
        loop += 1
        value = (value * subject) % modulus
    return result


def apply_loops(value, subject, loops):
    for _ in range(loops):
        value = (value * subject) % modulus
    return value

def calculate(public_keys, part=1):


    print(f'\nCalculate part {part} {public_keys=}')

    loop_sizes = get_loop_sizes(public_keys)

    encryption_keys = [apply_loops(1, public_keys[1-i], loops) for i, loops in enumerate(loop_sizes)]

    if encryption_keys[0] != encryption_keys[1]:
        print(f'Error, keys do not match: {encryption_keys}')
        return None
    
    result=encryption_keys[0]
    print(f"Result: {result}")
    return result


if __name__ == '__main__':
    assert(calculate([5764801, 17807724], part=1) == 14897079)
    calculate([8335663, 8614349], part=1)


# vim: et:ai:sw=4:ts=4
