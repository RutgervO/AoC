#!/usr/bin/env python3


from collections import deque

def calculate(startcups, moves=100, part=1, verbose=False):

    def debug(value):
        if verbose:
            print(value)

    class Cup:
        value = None
        next = None

        def __init__(self, value, next = None):
            self.value = value
            self.next = next

        def __gt__(self, other):
            return self.value > other.value

        def __str__(self):
            return str(self.value)

        def get_next(self, count):
            point = self.next
            result = []
            for _ in range(count):
                yield point
                point = point.next

        def get_next_str(self, count):
            return list(map(str, self.get_next(count)))

        def get_str_values(self, count):
            result = self.__str__()
            if count > 1:
                result += self.next.get_str_values(count - 1)
            return result

    cups = list(map(lambda x: Cup(int(x)), startcups))
    if part == 2:
        cups.extend(map(Cup, range(max(cups).value + 1, 1000001)))
    last_cup = cups[-1]
    for cup in cups:
        last_cup.next = cup
        last_cup = cup
    index = {cup.value: cup for cup in cups}

    len_cups = len(cups) 
    max_cup = max(cups).value
    
    print(f'\nPlaying {startcups} for {moves} moves, part {part}, {len_cups} cups')

    current_cup = cups[0]

    for move in range(moves):
        if part == 1:
            debug(f'\n-- move {move + 1} --\ncups: {current_cup.get_str_values(9)}\ncurent: {current_cup}')
        else:
            debug(f'\n-- move {move + 1} --\ncurent: {current_cup}')

        pick3 = list(current_cup.get_next(3))
        pick3_values = [cup.value for cup in pick3]

        debug(f'pick: {pick3_values}')

        new_value = current_cup.value
        while (new_value := ((max_cup + new_value - 2) % max_cup) + 1) in pick3_values:
            pass

        debug(f'destination: {new_value}')

        new_cup = index[new_value]

        current_cup.next=pick3[2].next
        pick3[2].next = new_cup.next
        new_cup.next = pick3[0]

        current_cup = current_cup.next
    
    current_cup = index[1]
    if part == 1:
        result = "".join(current_cup.get_next_str(8))
        print(f"{result=}")
        return result

    cup1 = current_cup.next
    cup2 = cup1.next
    result = cup1.value * cup2.value
    print(f'{cup1} * {cup2} => {result=}')
    return result

if __name__ == '__main__':
    assert(calculate('389125467', moves=10, part=1) == "92658374")
    assert(calculate('389125467', moves=100, part=1) == "67384529")
    assert(calculate('496138527',moves=100, part=1) == '69425837')

    assert(calculate('389125467', moves=10000000, part=2, verbose=False) == 149245887792)
    assert(calculate('496138527',moves=10000000, part=2) == 218882971435)

# vim: et:ai:sw=4:ts=4
