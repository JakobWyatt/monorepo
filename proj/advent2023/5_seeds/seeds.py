import sys

def parse_input(input):
    seeds = [int(x) for x in input[0].split(': ')[1].split(' ')]
    maps = []
    cur_map = []
    for line in input[2:]:
        if not line:
            maps.append(cur_map)
            cur_map = []
        else:
            cur_map.append([int(x) for x in line.split(' ')])
    return seeds, maps

def map_int(num, map):
    if num >= map[1] and num < map[1] + map[2]:
        return num - map[1] + map[0]
    else:
        return None

def rev_map_int(num, map):
    if num >= map[0] and num < map[0] + map[2]:
        return num - map[0] + map[1]
    else:
        return None

def def_map(num, maps):
    #print(f"seed {num}, maps {maps}")
    for map in maps:
        res = map_int(num, map)
        if res is not None:
            return res
    return num

def rev_def_map(num, maps):
    for map in maps:
        res = rev_map_int(num, map)
        if res is not None:
            return res
    return num

def seed2loc(seed, maps):
    loc = seed
    for map in maps:
        loc = def_map(loc, map)
    return loc

def loc2seed(loc, maps):
    seed = loc
    for map in reversed(maps):
        seed = rev_def_map(seed, map)
    return seed

def problem1(seeds, maps):
    print(min([seed2loc(x, maps) for x in seeds]))

def problem2(seeds, maps):
    locs = []
    for i in range(len(seeds) // 2):
        print("done one")
        start = seeds[i * 2]
        length = seeds[i * 2 + 1]
        locs.append(min([seed2loc(seed, maps) for seed in range(start, start + length)]))

def test_seed(seed, seeds):
    for i in range(len(seeds) // 2):
        start = seeds[i * 2]
        length = seeds[i * 2 + 1]
        if seed >= start and seed < start + length:
            return True
    return False

def problem2_fast(seeds, maps):
    i = 0
    while True:
        if test_seed(loc2seed(i, maps), seeds):
            print(f"the answer is {i}")
            return
        elif i % 1000000 == 0:
            print(i)
        i += 1

def main():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    seeds, maps = parse_input(input)
    problem2_fast(seeds, maps)

if __name__ == "__main__":
    main()
