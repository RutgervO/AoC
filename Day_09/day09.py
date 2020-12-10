#!/usr/bin/env python3

def two_in_window(swindow, number):
    swindow.sort()
    window_size = len(swindow)
    for x in range(0, window_size - 1):
        for y in range(x+1, window_size):
            total = swindow[x] + swindow[y]
            if total == number:
                return True
            if total > number:
                break;


def find_first_error(numbers, window_size):
    window_pos = 0
    for i in range(window_size, len(numbers)):
        number = numbers[i]
        if not two_in_window(numbers[window_pos:i], number):
            return number
        window_pos += 1
    return None


with open("input", "rt") as f:
    lines = list(f)

print(f"{len(lines)} lines read.")

numbers = [int(_) for _ in lines]

print(f"Largest number: {max(numbers)}")

first_error = find_first_error(numbers, 25)
print(f"First error: {first_error}")

# Part 2:
for i in range(0, len(numbers)):
    total = 0
    for j in range(i, len(numbers)):
        total += numbers[j]
        if i != j and total == first_error:
            the_set = numbers[i:j+1]
            the_set.sort()
            min_max_sum = min(the_set) + max(the_set)
            print(f"Pos {i} through {j} min_max_sum: {min_max_sum} sorted: '{the_set}'")
        if total > first_error:
            break;
        


# vim: et:ts=4:sw=4:ai
