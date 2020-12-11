#!/usr/bin/env python3

with open('input', 'rt') as f:
    lines = f.readlines()

print(f"{len(lines)} lines read.")

groups = []

group_id = 0
group = {}
group['set'] = set()
group['people'] = 0
groups.append(group)

for line in lines:
    if len(line.strip()) == 0:
        group_id += 1
        group = {}
        group['set'] = set()
        group['people'] = 0
        groups.append(group)
    else:
        new_set = set(_ for _ in line.strip())
        group['set'].update(new_set)
        if group['people'] == 0:
            group['int'] = new_set
        else:
            group['int'] = group['int'] & new_set
        group['people'] += 1

print(f"{group_id} groups found")

total = 0
total_int = 0
for group in groups:
    total += len(group['set'])
    total_int += len(group['int'])

print(f'{total} total counts (part 1, union)')

print(f'{total_int} total counts (part 2, intersection)')

    



# vim: ai:sw=4:ts=4:et
