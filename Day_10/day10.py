#!/usr/bin/env python3

from collections import defaultdict
from functools import lru_cache

with open('input', 'rt') as f:
    lines = list(f)

print(f"{len(lines)} lines read")

numbers = [int(_) for _ in lines]
# Note: these are all >0 and are all different

numbers.sort()
device_jolts = max(numbers) + 3
numbers.append(device_jolts) # add devices adapter

dist = defaultdict(int)

jolt = 0
for adapter in numbers:
    diff = adapter - jolt
    if not (0 <= diff <= 3):
        print(f"ERROR {diff=}")
    jolt = adapter
    dist[diff] += 1

print(f"Distribution: {dist}")
print(f"1 * 3: {dist[1] * dist[3]}")

# Part 2... brute force!?

# First way is to use all adapters
# Any other way means omitting one or more
# So there are 2^(107-1) possibilities (you always have to use your own device)

# Recursive
@lru_cache()
def how_many_ways(end_pos, max_jolt, pos, jolt):
    result = 0
    adapter = numbers[pos]
    diff = adapter - jolt
    if diff <= 3:
        if pos == end_pos - 1:
            result = 1
        else:
            result = how_many_ways(end_pos, max_jolt, pos + 1, jolt) + \
                     how_many_ways(end_pos, max_jolt, pos + 1, adapter) 

    return result


count = how_many_ways(len(numbers), device_jolts, 0, 0)

print(f"{count} possible ways")


# vim: et:ts=4:sw=4:ai
