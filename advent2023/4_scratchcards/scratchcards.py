import sys

def parse_list(list):
    nums = []
    for num in list.split(' '):
        if num:
            nums.append(int(num))
    return nums

def parse_input(input):
    cards = {}
    for line in input:
        a = line.split(': ')
        card = int(a[0][5:])
        winners, mine = a[1].split(' | ')
        cards[card] = (parse_list(winners), parse_list(mine))
    return cards

def get_num_winners(mines, winners):
    num_winners = 0
    for mine in mines:
        if mine in winners:
            num_winners += 1
    return num_winners

def problem1(cards):
    total = 0
    for winners, mines in cards.values():
        num_winners = get_num_winners(mines, winners)
        if num_winners != 0:
            total += 2 ** (num_winners - 1)
    print(f"{total} total points")

def problem2(cards):
    copies = [1] * len(cards)
    for i, c in enumerate(cards.values()):
        winners, mines = c
        num_winners = get_num_winners(mines, winners)
        for j in range(i + 1, i + num_winners + 1):
            copies[j] += copies[i]
    print(sum(copies))

def main():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    problem2(parse_input(input))

if __name__ == "__main__":
    main()
