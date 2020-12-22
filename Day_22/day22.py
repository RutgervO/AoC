#!/usr/bin/env python3

import copy


def calculate(filename, part=1, verbose=False):

    def debug(value):
        if verbose:
            print(value)

    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"\nPart {part}, {filename}, {len(lines)} lines")
    
    hands = []
    line = lines.index("")
    hands.append(list(map(int, lines[1:line])))
    hands.append(list(map(int, lines[line+2:])))

    debug(f"{hands=}")
    
    def recursive_combat(hands, part):
        memory = []

        debug(f"Game on! {hands=}")

        while all(len(hand) > 0 for hand in hands):
            if part == 2 and hands in memory:
                debug(f"Recursion limit! Player 1 wins")
                return 0
            memory.append(copy.deepcopy(hands))

            dealt = [ hand.pop(0) for hand in hands ]

            if part == 2 and all(len(hand) >= card for card, hand in zip(dealt, hands)):
                # Recurse!
                winner = recursive_combat([hand[:card] for card, hand in zip(dealt, hands)], part)
                hands[winner].append(dealt[winner])
                hands[winner].append(dealt[1 - winner]) # only works for 2 players
            else:
                winner = dealt.index(max(dealt))
                dealt.sort(reverse=True)
                hands[winner].extend(dealt)

            debug(f"{hands=}")
        debug(f"{winner=}")
        return winner

    hand = hands[recursive_combat(hands, part)]
    result = sum(card * value for card,value in zip(hand, range(len(hand), 0, -1)))
    print(f"{result=}")
    return result


def test(value, func, *args, **kwargs):
    result = func(*args, **kwargs)
    if result == value:
        print(f"\nCORRECT! {func.__name__} {args} => {result}")
    else:
        print(f"\nWRONG!   {func.__name__} {args} => {result} but should be {value}")


if __name__ == '__main__':
    test(306, calculate, 'demo-input', part=1, verbose=False)
    calculate('input', part=1)

    test(291, calculate, 'demo-input', part=2, verbose=False)
    calculate('input', part=2, verbose=False)


# vim: et:ai:sw=4:ts=4
