import sys

def finditem(s):
    return set(s[0]) & set(s[1]) & set(s[2])

def priority(c):
    point = ord(c.lower()) - ord('a') + 1
    if c.isupper():
        return point + 26
    return point 

def main():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    badges = []
    for i in range(len(input) // 3):
        badges.append(finditem(input[i * 3:i * 3 + 3]).pop())
    print(sum(priority(x) for x in badges))

if __name__ == "__main__":
    main()
