#!/usr/bin/env python3

with open("input", "rt") as f:
    lines = f.readlines()

print(f"{len(lines)} lines read.")

line_length = len(lines[0].strip())

print(f"lines are {line_length} long.")

posx = 0
posy = 0

stepx = 3
stepy = 1

targety = len(lines)

count = 0

while posy < targety:
    line = lines[posy]
    hit = (line[posx] == '#')
    if hit:
        count += 1
    print(f"{line[0:posx]}[{line[posx]}]{line[posx+1:line_length]} {posx},{posy}: {hit}")
    posx = (posx + stepx) % line_length
    posy = posy + stepy

print(f"{count} trees hit")

# vim: ai:ts=4:sw=4:et:syntax=python 
