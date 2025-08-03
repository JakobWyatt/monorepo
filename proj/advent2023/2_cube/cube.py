import sys

# red, green, blue
def parse_input(input):
    games = {}
    for line in input:
        rgb_all = []
        game = int(line.split(': ')[0][5:])
        hands = line.split(': ')[1].split('; ')
        for hand in hands:
            rgb = [0, 0, 0]
            groups = hand.split(', ')
            for group in groups:
                s = group.split(' ')
                num, color = int(s[0]), s[1]
                if color == "red":
                    rgb[0] = num
                if color == "green":
                    rgb[1] = num
                if color == "blue":
                    rgb[2] = num
            rgb_all.append(rgb)
        games[game] = rgb_all
    return games

def problem1(input):
    # which games would have been possible given (12, 13, 14)?
    # boxes are replaced
    rgb = [12, 13, 14]
    id_sum = 0
    for gamenum, hands in input.items():
        possible = True
        for hand in hands:
            if hand[0] > rgb[0] or hand[1] > rgb[1] or hand[2] > rgb[2]:
                possible = False
        if possible:
            print(f"Game {gamenum} possible")
            id_sum += gamenum
    print(f"id sum {id_sum}")

def min_cubes(hands):
    rgb = [0, 0, 0]
    for hand in hands:
        for i in range(3):
            rgb[i] = max(rgb[i], hand[i])
    return rgb

def cube_power(rgb):
    return rgb[0] * rgb[1] * rgb[2]

def problem2(input):
    sum_power = 0
    for gamenum, hands in input.items():
        sum_power += cube_power(min_cubes(hands))
    print(f"sum: {sum_power}")

def main():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    problem2(parse_input(input))

if __name__ == "__main__":
    main()
