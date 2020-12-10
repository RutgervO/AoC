from pathlib import Path

def main():
    
    with open("input_sorted", "r") as text_file:
        numbers = [int(x) for x in text_file.readlines()]
    
    max_index = len(numbers)
    wanted = 2020

    for index in range(0, max_index - 2): # -2 because we need 3 numbers at the least
        print(f'{index}...')
        n1 = numbers[index]
        if n1 > wanted:
            break
        for index2 in range(index + 1, max_index - 1):
            n2 = numbers[index2]
            if n1 + n2 > wanted:
                break
            for index3 in range(index2 + 1, max_index):
                n3 = numbers[index3]
                the_sum = n1 + n2 + n3
                if the_sum == wanted:
                    print(f"FOUND! {n1} + {n2} + {n3} = {wanted}. {n1} * {n2} * {n3} = {n1 * n2 * n3}")
                    return
                if the_sum > wanted:
                    # Since the list is sorted the results will all be too large... break
                    break

    print('Nothing found!')

if __name__ == '__main__':
    main()

# vim: ai:ts=4:sw=4:et
