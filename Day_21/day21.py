#!/usr/bin/env python3

from collections import defaultdict


def calculate(filename, part=1, verbose=False):

    def debug(value):
        if verbose:
            print(value)

    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"\nPart {part}, {filename}, {len(lines)} lines")

    foods = [] # list of set of ingredients
    food_allergens = [] # list of set of allergens (for each food)
    all_ingredients = set()
    all_allergens = set()
    count_ingredients = defaultdict(int)

    for line in lines:
        contains = line.index("(")

        foods.append(words := set(line[ : contains - 1].split(" ")))
        all_ingredients.update(words)
        for ingredient in words:
            count_ingredients[ingredient] += 1

        food_allergens.append(words := set(line[contains + 10 : -1].split(", ")))
        all_allergens.update(words)

        debug(f"{line=}: {foods[-1]=} {food_allergens[-1]=}")

    # Find list of candidates per allergen
    suspect_ingredients = set()
    combinations = {} # allergen -> suspected ingredients

    for allergen in all_allergens:
        
        suspects = all_ingredients.copy()

        # process only foods that contain this allergen
        for index, allergens in enumerate(food_allergens):
            if allergen in allergens:
                suspects &= foods[index]

        debug(f"Suspect {allergen} is in {suspects}")
        suspect_ingredients.update(suspects)
        combinations[allergen] = suspects


    # Safe ingredients are the ones that are not suspect
    safe_ingredients = all_ingredients - suspect_ingredients

    # Count how often the safe ingredients appear
    count = 0
    for ingredient in safe_ingredients:
        count += count_ingredients[ingredient]

    if part == 1:
        print(f"{count=}")
        return count

    # reduce until each allergen has one ingredient
    count = 1
    singles = set()
    while count > 0:
        count = 0
        for allergen, suspects in combinations.items():
            if len(suspects) == 1:
                singles.update(suspects)
            else:
                count += 1
                suspects -= singles
    
    result=",".join([allergen.pop() for _, allergen in sorted(combinations.items())])
    print(f"{result=}")
    return result


def test(value, func, *args, **kwargs):
    result = func(*args, **kwargs)
    if result == value:
        print(f"\nCORRECT! {func.__name__} {args} => {result}")
    else:
        print(f"\nWRONG!   {func.__name__} {args} => {result} but should be {value}")


if __name__ == '__main__':
    test(5, calculate, 'demo-input', part=1, verbose=False)
    calculate('input', part=1)

    test("mxmxvkd,sqjhc,fvjkl", calculate, 'demo-input', part=2, verbose=False)
    calculate('input', part=2)


# vim: et:ai:sw=4:ts=4
