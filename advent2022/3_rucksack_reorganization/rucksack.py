import sys

def finditem(s):
    midpoint = len(s) // 2
    return set(s[:midpoint]) & set(s[midpoint:])

def priority(c):
    point = ord(c.lower()) - ord('a') + 1
    if c.isupper():
        return point + 26
    return point 

def main():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    print(sum(priority(finditem(rucksack).pop()) for rucksack in input))

if __name__ == "__main__":
    main()
