import sys

def problem1():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    sum = 0
    for line in input:
        digits = [c for c in line if c.isdigit()]
        print(f"first: {digits[0]}, last: {digits[-1]}")
        sum += int(digits[0]) * 10 + int(digits[-1])
    print(f"sum: {sum}")

digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

# On full match, (True, 5)
# On partial match, (True, None)
def prefix_match(prefix):
    partial_match = False
    # hack to get digit num
    for i, candidate in enumerate(digits):
        if candidate.startswith(prefix):
            partial_match = True
            if candidate == prefix:
                return (True, i + 1)
    return (partial_match, None)

def tokenize_string(line):
    prefix = ""
    tokens = []
    for c in line:
        if c.isdigit():
            tokens.append(int(c))
            prefix=""
        else:
            prefix += c
            has_match, match = prefix_match(prefix)
            # full match, tokenize
            if has_match and match is not None:
                tokens.append(match)
                prefix = prefix[1:]
            # partial match, keep going, do nothing
            # no match, remove from front of str until empty or we match
            if not has_match:
                while len(prefix) != 0 and not prefix_match(prefix)[0]:
                    prefix = prefix[1:]
                if len(prefix) != 0:
                    print(prefix)
    return tokens

def problem2():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    sum = 0
    for line in input:
        tokens = tokenize_string(line)
        res = tokens[0] * 10 + tokens[-1]
        print(res)
        sum += res
    print(f"sum: {sum}")

if __name__ == "__main__":
    problem2()
