#!/usr/bin/env python3


from collections import deque

def calculate(startcups, moves=100, part=1, verbose=False):

    def debug(value):
        if verbose:
            print(value)

    cups = deque(map(int, startcups))
    if part == 2:
        cups.extend(range(max(cups) + 1, 1000001)) 
    len_cups = len(cups) 
    max_cup = max(cups)
    
    print(f'\nPlaying {startcups} for {moves} moves, part {part}, {len_cups} cups')


    buffersize = 40
    last_deviations = deque([0], buffersize)
    last_positions = deque([0], buffersize)
    last_hits = deque([0], buffersize)
    current_deviation = 1
    current_history = 1
    for move in range(moves):
        if not (move - 1) % 10000:
            print(f'Move {move+1} {current_deviation=} {current_history=}')
        current_cup = cups[0]

        if part == 1:
            debug(f'\n-- move {move + 1} --\ncups: {", ".join(map(str, cups))}\ncurent: {current_cup}')
        else:
            debug(f'\n-- move {move + 1} --\ncurent: {current_cup}')

        # current is always 0: pick the next 3
        current_cup = cups.popleft()
        pick3 = [cups.popleft() for _ in range(3)]
        cups.appendleft(current_cup)

        debug(f'pick: {pick3}')

        new_cup = current_cup
        while (new_cup := ((max_cup + new_cup - 2) % max_cup) + 1) in pick3:
            pass

        debug(f'destination: {new_cup}')

        #new_pos = cups.index(new_cup)  ## Too slow
        # Expect a pattern to occur - guess based on previous values

        max_deviation = max(last_deviations)
        if max_deviation > current_deviation:
            current_deviation += 1
        if max_deviation < current_deviation:
            current_deviation -= 1
        if last_hits.count(0) > 1:
            current_history = min(current_history + 1, buffersize)
        if last_hits.count(0) == 0:
            if min(last_hits) > -current_history:
                current_history = max(current_history - 1, 2)
        
        hit = 0 # no hit, otherwise abs negative position in cache
        guesses = set()
        positions = list(last_positions)[-current_history:]
        for i in range(-1, -len(positions)-1, -1):
            for deviation in range(- current_deviation, current_deviation + 1):
                guess = positions[i] + deviation
                if guess not in guesses and (0 <= guess < len_cups - 3) and cups[guess] == new_cup:
                    hit = i
                    new_pos = guess
                    break
                guesses.add(guess)
            else:
                continue
            break
        if not hit:
            cups.reverse()
            new_pos = len_cups - 1 - 3 - cups.index(new_cup)
            cups.reverse()
            print(f"Bad guesses {move=} {new_pos=} {guesses=}\n{current_history=} {current_deviation=}\n{last_positions=}\n{last_deviations=}\n{last_hits=}")

        deviation = min(abs(pos - new_pos) for pos in last_positions)
        last_positions.append(new_pos)
        last_deviations.append(deviation)
        last_hits.append(hit)

        cups.rotate(-(new_pos + 1))

        pick3.reverse()
        cups.extendleft(pick3)

        cups.rotate(new_pos)
    
    # Rotate so that 1 is first
    cups.rotate(-cups.index(1))
    cups.popleft()

    if part == 1:
        debug(f"\nfinal:{cups}")
        result = "".join(map(str, list(cups)))
        print(f"{result=}")
        return result

    result = cups[0] * cups[1]
    print(f'{cups[0]} * {cups[1]} => {result=}')
    return result

if __name__ == '__main__':
    assert(calculate('389125467', moves=10, part=1) == "92658374")
    assert(calculate('389125467', moves=100, part=1) == "67384529")
    #calculate('496138527',moves=100, part=1)
    assert(calculate('496138527',moves=100, part=1) == '69425837')

    #assert(calculate('389125467', moves=150000, part=2, verbose=False) == '149245887792')
    assert(calculate('389125467', moves=10000000, part=2, verbose=False) == '149245887792')
    #assert(calculate('389125467', moves=10000000, part=2, verbose=True) == '149245887792')
    #calculate('496138527',moves=10000000, part=2)
    #calculate('496138527',moves=10000000, part=2)

# vim: et:ai:sw=4:ts=4
