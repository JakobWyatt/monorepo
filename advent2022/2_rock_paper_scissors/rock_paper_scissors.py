import sys

class Play:
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

def outcome_score(opponent, ego):
    if opponent == ego:
        return 3 # draw
    if (opponent == Play.ROCK and ego == Play.PAPER
        or opponent == Play.PAPER and ego == Play.SCISSORS
        or opponent == Play.SCISSORS and ego == Play.ROCK):
        return 6 # win
    return 0 # loss

def score(games):
    total_score = 0
    for opponent, ego in games:
        total_score += ego + outcome_score(opponent, ego)
    return total_score

def to_play(s):
    if s == 'A' or s == 'X':
        return Play.ROCK
    if s == 'B' or s == 'Y':
        return Play.PAPER
    if s == 'C' or s == 'Z':
        return Play.SCISSORS
    return None

def parse_games(input):
    parsed = []
    for game in input:
        parsed.append((to_play(game[0]), to_play(game[2])))
    return parsed

def main():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    print(score(parse_games(input)))

if __name__ == "__main__":
    main()
