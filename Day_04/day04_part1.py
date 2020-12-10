#!/usr/bin/env python3

from parse import *

# Read linex
with open("input", "rt") as f:
	lines = f.readlines()

print(f"{len(lines)} lines read.")

# Make list of dicts

i = 0   # working on this entry, increase when empty line
records = []    # List of dicts

for line in lines:
    # empty line!
    if len(line.strip()) == 0:
        i += 1
    else:
        # get a/the dict
        if i < len(records):
            record = records[i]
        else:
            record = {}
            records.append(record)
        
        # parse! split on spaces
        for entry in line.split(" "):
            parsed = parse("{key:l}:{value:S}", entry)
            record[parsed["key"]] = parsed["value"]
        
print(f"{i} entries parsed.")

# Count!
count_valid_all = 0         # All keys present
count_valid_required = 0    # All but optional key(s) present

required_keys = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
optional_keys = {'cid'}
all_keys = required_keys | optional_keys # set union

print(f"Required: {required_keys}")
print(f"Optional: {optional_keys}")
print(f"All:      {all_keys}")

#    byr (Birth Year)
#    iyr (Issue Year)
#    eyr (Expiration Year)
#    hgt (Height)
#    hcl (Hair Color)
#    ecl (Eye Color)
#    pid (Passport ID)
#    cid (Country ID)

for record in records:
    keys = set(record.keys())
    all_valid = (keys & all_keys) == all_keys
    required_valid = (keys & required_keys) == required_keys
    count_valid_all += (1 if all_valid else 0)
    count_valid_required += (1 if required_valid else 0)
    print(f"{keys} all: {all_valid} opt: {required_valid}")
    
    
print()
print(f"Valid with all keys: {count_valid_all}")
print(f"Valid without optional keys: {count_valid_required}")

# vim: ai:ts=4:sw=4:et
