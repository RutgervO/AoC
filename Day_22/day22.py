#!/usr/bin/env python3


def calculate(filename, part=1, verbose=False):

    def debug(value):
        if verbose:
            print(value)

    with open(filename, "rt") as f:
        lines = [_.strip() for _ in f]

    print(f"\nPart {part}, {filename}, {len(lines)} lines")
    
    line = lines.index("")
    hands = [list(map(int, lines[1:line])), list(map(int, lines[line+2:]))]

    debug(f"{hands=}")
    
    def recursive_combat(hands, part):
        memory = set()

        debug(f"Game on! {hands=}")

        while all(len(hand) > 0 for hand in hands):
            if part == 2:
                tupled = tuple(map(tuple, hands))
                if tupled in memory:
                    debug(f"Recursion limit! Player 1 wins")
                    return 0
                memory.add(tupled)

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


if __name__ == '__main__':
    assert(calculate('demo-input', part=1) == 306)
    calculate('input', part=1)

    assert(calculate('demo-input', part=2) == 291)
    calculate('input', part=2)


# vim: et:ai:sw=4:ts=4
