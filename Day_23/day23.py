#!/usr/bin/env python3

def calculate(startcups, moves=100, part=1, verbose=False):

    def debug(value):
        if verbose:
            print(value)

    cups = list(map(int, startcups))
    if part == 2:
        cups.extend(range(max(cups) + 1, 1000001)) 
    len_cups = len(cups) 
    max_cup = max(cups)
    
    print(f'\nPlaying {startcups} for {moves} moves, part {part}, {len_cups} cups')

    current_pos = 0
    current_cup = cups[0]

    for move in range(moves):
        if part == 1:
            debug(f'\n-- move {move + 1} --\ncups: {", ".join(map(str, cups))}\ncurent: {current_cup}')
        else:
            debug(f'\n-- move {move + 1} --\ncurent: {current_cup}')

        pick_right = cups[current_pos + 1:current_pos + 4] 
        pick_left = cups[0:max(0, current_pos + 4 - len_cups)]
        pick3 = pick_right + pick_left

        debug(f'pick: {pick3}')

        for cup in pick3:
            cups.remove(cup)  ## ToDo: slow

        new_cup = current_cup
        for _ in range(4):
            new_cup -= 1
            if new_cup == 0:
                new_cup = max_cup
            if new_cup not in pick3:
                break

        debug(f'destination: {new_cup}')

        new_pos = cups.index(new_cup)
        cups = cups[0:new_pos + 1] + pick3 + cups[new_pos + 1:]    ## ToDo: slow

        # There seems to be an unwritten rule: the previous current_cup needs to stay in the same position
        current_pos = cups.index(current_cup)

        current_pos = (current_pos + 1) % len_cups
        current_cup = cups[current_pos]
    
    if part == 1:
        debug(f"\nfinal:{cups}")
        result = "".join(map(str, (cups + cups)[cups.index(1) + 1:][:8]))
        print(f"{result=}")
        return result

    results = (cups + cups[:2])[cups.index(1)+1:][:2]
    result = results[0] * results[1]
    print(f'{results} => {result=}')
    return result

if __name__ == '__main__':
    assert(calculate('389125467', moves=10, part=1) == "92658374")
    assert(calculate('389125467', moves=100, part=1) == "67384529")
    #calculate('496138527',moves=100, part=1)
    assert(calculate('496138527',moves=100, part=1) == '69425837')

    assert(calculate('389125467', moves=10000000, part=2) == '149245887792')
    calculate('496138527',moves=10000000, part=2)
    #calculate('input', part=2)

# vim: et:ai:sw=4:ts=4
