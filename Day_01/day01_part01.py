from pathlib import Path

def main():
    
    with open("input_sorted", "r") as text_file:
        numbers = [int(x) for x in text_file.readlines()]
    
    max_index = len(numbers)
    wanted = 2020

    for index in range(0, max_index - 1): # -1 because we can't add two numbers if there is only 1
        print(f'{index}...')
        n1 = numbers[index]
        for index2 in range(index + 1, max_index):
            n2 = numbers[index2]
            the_sum = n1 + n2
            if the_sum == wanted:
                print(f"FOUND! {n1} + {n2} = {wanted}. {n1} * {n2} = {n1 * n2}")
                return
            if the_sum > wanted:
                # Since the list is sorted the results will all be too large... break
                break

    print('Nothing found!')

if __name__ == '__main__':
    main()

# vim: ai:ts=4:sw=4:et
