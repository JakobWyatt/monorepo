import sys

def add_symbol(c, only_gears):
    return ((not only_gears and c != '.' and not c.isdigit())
            or (only_gears and c == '*'))

 # [(x, y)] top left 0, 0
def get_symbol_list(input, only_gears):
    symbol_list = []
    for yi, line in enumerate(input):
        for xi, c in enumerate(line):
            if add_symbol(c, only_gears):
                symbol_list.append((xi, yi))
    return symbol_list

# [(number, yi, x_min, x_max)]
def get_number_list(input):
    number_list = []
    for yi, line in enumerate(input):
        number = None
        x_min = None
        for xi, c in enumerate(line):
            if c.isdigit():
                if number is None:
                    x_min = xi
                    number = int(c)
                else:
                    number = number * 10 + int(c)
            # add number to the list if not digit or out of space
            if number is not None and (not c.isdigit() or xi == len(line) - 1):
                number_list.append((number, yi, x_min, xi - 1))
                number = None
    return number_list

def is_part_number(number, symbols):
    for symbol in symbols:
        if adjacent(number, symbol):
            return True
    return False

# add all part numbers in engine schematic nxn
def problem1(symbols, parts):
    sum = 0
    for part in parts:
        if is_part_number(part, symbols):
            sum += part[0]
    print(f"sum: {sum}")

def satisfies_x(xi, x_low, x_high):
    return ((x_low <= xi and x_high >= xi)
        or x_low == xi + 1 or x_high == xi - 1)

def adjacent(number, symbol):
    satisfies_y = (number[1] >= symbol[1] - 1) and (number[1] <= symbol[1] + 1)
    return satisfies_y and satisfies_x(symbol[0], number[2], number[3])

def get_adj_parts(gear, parts):
    adj_parts = []
    for part in parts:
        if adjacent(part, gear):
            adj_parts.append(part)
    return adj_parts

def problem2(gears, parts):
    sum = 0
    for gear in gears:
        adj_parts = get_adj_parts(gear, parts)
        if len(adj_parts) == 2:
            sum += adj_parts[0][0] * adj_parts[1][0]
    print(f"sum {sum}")

def main():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    problem2(get_symbol_list(input, True), get_number_list(input))

if __name__ == "__main__":
    main()
