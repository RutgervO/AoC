#!/usr/bin/env python3

"""
    rows 0 - 127: F = 0, B = 1, 7 bits
    columns: 0-7: L = 0, R = 1, 3 bits
"""

def parse_seat_code(code):
    code = code.strip()
    r = {}
    r['code'] = code
    if len(code) != 10:
        print(f"ERROR can not parse code '{code}'")
        return r
    bin_code = code.replace('F', '0').replace('B', '1').replace('L', '0').replace('R', '1')
    r['bin'] = bin_code
    id = int(bin_code, 2)
    r['id'] = id
    row = id // 8
    r['row'] = row
    col = id % 8
    r['col'] = col
    return r


with open("input", "rt") as f:
    lines = f.readlines()

print(f"{len(lines)} lines read.")

seats = {}  # store dict per seat id
max_seat_id = -1

for line in lines:
    seat = parse_seat_code(line)
    id = seat['id']
    print(seat)
    seats[id] = seat
    max_seat_id = max(max_seat_id, id)

print(f'PART 1: Largest id: {max_seat_id}')

#### PART 2

""" so we need to exclude the first and last row """
last_row = -1
first_row = 1024 # 2 ^ 10

for id, seat in seats.items():
    first_row = min(first_row, seat['row'])
    last_row = max(last_row, seat['row'])

print(f"{first_row=} {last_row=}")

# create set of eligible seats
empty_seats = set(range((first_row * 8) + 8, last_row * 8))

for id, seat in seats.items():
    if first_row < seat['row'] < last_row:
        empty_seats.discard(id)

print(f"Empty seat ids between first and last occupied rows: {empty_seats}")

# vim: ai:ts=4:sw=4:et
