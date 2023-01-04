import sys
from enum import Enum

## enums and helpers

class Play(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

class Outcome(Enum):
    LOSE = 0
    DRAW = 3
    WIN = 6

def to_play(s):
    if s == 'A':
        return Play.ROCK
    if s == 'B':
        return Play.PAPER
    if s == 'C':
        return Play.SCISSORS
    return None

def to_outcome(s):
    if s == 'X':
        return Outcome.LOSE
    if s == 'Y':
        return Outcome.DRAW
    if s == 'Z':
        return Outcome.WIN
    return None

## core logic

def find_shape(opponent, outcome):
    if outcome == Outcome.DRAW:
        return opponent
    if outcome == Outcome.WIN:
        return Play((opponent.value + 1) % 3)
    if outcome == Outcome.LOSE:
        return Play((opponent.value - 1) % 3)

def score(games):
    total_score = 0
    for opponent, outcome in games:
        total_score += outcome.value + 1 + find_shape(opponent, outcome).value
    return total_score

## parsing

def parse_games(input):
    parsed = []
    for game in input:
        parsed.append((to_play(game[0]), to_outcome(game[2])))
    return parsed

def main():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    print(score(parse_games(input)))

if __name__ == "__main__":
    main()
