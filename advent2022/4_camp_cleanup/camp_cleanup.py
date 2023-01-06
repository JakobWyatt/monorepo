import sys

def parse_ranges(input):
    ranges = []
    for pair in input:
        x, y = pair.split(',')
        ranges.append((parse_range(x), parse_range(y)))
    return ranges

def parse_range(text):
    first, last = text.split('-')
    return int(first), int(last) + 1

def is_contained(x1, x2, y1, y2):
    if x1 > y1:
        return x2 <= y2
    elif x1 < y1:
        return x2 >= y2
    else:
        return True

def is_overlapping(x1, x2, y1, y2):
    # make x1, x2 the lower range
    if x1 > y1:
        x1, x2, y1, y2 = y1, y2, x1, x2
    return x2 > y1

def count_cond(ranges, f):
    n = 0
    for r in ranges:
        if f(r[0][0], r[0][1], r[1][0], r[1][1]):
            print(r)
            n += 1
    return n

def main():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    print(count_cond(parse_ranges(input), is_overlapping))

if __name__ == "__main__":
    main()
