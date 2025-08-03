import sys
from enum import Enum

class Dir(Enum):
    L = 0
    R = 1
    U = 2
    D = 3

class Move:
    def __init__(self, dir: Dir, dist: int):
        self.dir = dir
        self.dist = dist

def parse_moves(input: list[str]):
    return [Move(Dir[x[0]], int(x[2:])) for x in input]

def move_head(cur, dir: Dir):
    if dir == Dir.L:
        return (cur[0] - 1, cur[1])
    if dir == Dir.R:
        return (cur[0] + 1, cur[1])
    if dir == Dir.U:
        return (cur[0], cur[1] + 1)
    if dir == Dir.D:
        return (cur[0], cur[1] - 1)

def find_locations_travelled(moves: list[Move]):
    h = (0, 0)
    t = (0, 0)
    locs = {t}
    for move in moves:
        for _ in range(move.dist):
            # move h first
            h = move_head(h, move.dir)
            # move diagonally?
            if h[0] != t[0] and h[1] != t[1]:
                # which way x
                if h[0] > t[0]:
                    t = (t[0] + 1, t[1])
                else:
                    t = (t[0] - 1, t[1])
                # which way y
                if h[1] > t[1]:
                    t = (t[0], t[1] + 1)
                else:
                    t = (t[0], t[1] - 1)
            else:
                # move y?
                if h[0] == t[0]:
    return locs

def main():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    moves = parse_moves(input)
    locs = find_locations_travelled(moves)
    print(len(locs))

if __name__ == "__main__":
    main()
