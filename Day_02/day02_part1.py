from parse import *

# Read

with open("input", "r") as f:
    lines = f.readlines()

print(f"{len(lines)} lines read.")

# Parse and count

correct = 0

for line in lines:
    parsed = parse("{from:d}-{to:d} {letter:l}: {password:S}", line)
    count = parsed["password"].count(parsed["letter"])
    result = (parsed["from"] <= count <= parsed["to"])
    if result:
        correct += 1
    print(f"{parsed}: {count} {result}")

print(f"{correct} correct passwords.")


# vim: ai:sw=4:ts=4:et:syn=on
