#!/usr/bin/env python3

from parse import *

def sanity_check(r):
    """
    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.
    """
    # Assume all keys are present - just parse them, return true if valid, false if not

    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    key = 'byr'
    p = parse("{v:4d}", r[key])
    if p is None:
        print(f"{key} parsed niet")
        return False
    v = int(p['v'])
    if v < 1920 or v > 2002:
        print(f"{key} value {v} out of range")
        return False

    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    key = 'iyr'
    p = parse("{v:4d}", r['iyr'])
    if p is None:
        print(f"{key} parsed niet")
        return False
    v = int(p['v'])
    if v < 2010 or v > 2020:
        return False

    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    key = 'eyr'
    p = parse("{v:4d}", r['eyr'])
    if p is None:
        print(f"{key} parsed niet")
        return False
    v = int(p['v'])
    if v < 2020 or v > 2030:
        return False

    # hgt (Height) - a number followed by either cm or in:
    #    If cm, the number must be at least 150 and at most 193.
    #    If in, the number must be at least 59 and at most 76.
    key = 'hgt'
    p = parse("{v:d}{u:2l}", r['hgt'])
    if p is None:
        print(f"{key} parsed niet")
        return False
    u = p['u']
    v = int(p['v'])
    if u == 'cm':
        if v < 150 or v > 193:
            return False
    elif u == 'in':
        if v < 59 or v > 76:
            return False
    else:
        return False # bad uom

    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    key = 'hcl'
    p = parse("#{v:6x}", r['hcl']) # attention: case insensitive, but input is all lower
    if p is None:
        print(f"{key} parsed niet")
        return False

    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    key = 'ecl'
    p = parse("{v:3l}", r['ecl'])
    if p is None:
        print(f"{key} parsed niet")
        return False
    v = p['v']
    if v not in {'amb','blu','brn','gry','grn','hzl','oth'}:
        return False

    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    key = 'pid'
    if len(r[key]) != 9:
        print(f"{key} has incorrect length")
        return False
    p = parse("{v:9d}", r['pid']) # Let op - accepteert ook kortere getallen < 9 digits!!!
    if p is None:
        print(f"{key} parsed niet")
        return False
    print(f"{key}: {v}")

    # cid (Country ID) - ignored, missing or not.

    return True

	
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
count_valid_required = 0    # All keys present, with or without optional keys
count_valid_required_values = 0 # All keys present, with or without optional, with good values

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
    values_valid = False
    if required_valid:
        values_valid = sanity_check(record)
    count_valid_all += 1 if all_valid else 0
    count_valid_required += 1 if required_valid else 0
    count_valid_required_values += 1 if values_valid else 0


    print(f"{record} all: {all_valid} opt: {required_valid} values: {values_valid}")
    
    
print()
print(f"Valid with all keys: {count_valid_all}")
print(f"Valid without optional keys: {count_valid_required}")
print(f"Valid without optional keys but with valid values: {count_valid_required_values}")

# vim: ai:ts=4:sw=4:et
