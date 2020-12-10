#!/usr/bin/env python3

def get_trees(lines, stepx, stepy):
    targety = len(lines)
    line_length = len(lines[0].strip())

    count = 0
    posx = 0
    posy = 0

    while posy < targety:
        line = lines[posy]
        hit = (line[posx] == '#')
        if hit:
            count += 1
        posx = (posx + stepx) % line_length
        posy = posy + stepy

    print(f"{stepx},{stepy}: {count} trees hit")
    return count


with open("input", "rt") as f:
    lines = f.readlines()

print(f"{len(lines)} lines read.")

product = 1
for x, y in [(1,1), (3,1), (5,1), (7,1), (1,2)]:
    count = get_trees(lines, x, y)
    product *= count
    
print(f"The product is {product}.")



# vim: ai:ts=4:sw=4:et:syntax=python 
