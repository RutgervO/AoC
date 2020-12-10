from parse import *

# Read

with open("input", "r") as f:
    lines = f.readlines()

print(f"{len(lines)} lines read.")

# Parse and count

correct = 0

for line in lines:
    parsed = parse("{pos1:d}-{pos2:d} {letter:l}: {password:S}", line)
    count = 1 if parsed["password"][parsed["pos1"] - 1] == parsed["letter"] else 0
    count += 1 if parsed["password"][parsed["pos2"] - 1] == parsed["letter"] else 0
    result = (count == 1)
    if result:
        correct += 1
    print(f"{parsed}: {count} {result}")

print(f"{correct} correct passwords.")


# vim: ai:sw=4:ts=4:et:syn=on
