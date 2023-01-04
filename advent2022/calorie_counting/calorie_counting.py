import sys

def chunks(lines):
    chunks = []
    chunk = []
    for l in lines:
        if l:
            chunk.append(l)
        elif chunk:
            chunks.append(chunk)
            chunk = []
    if chunk:
        chunks.append(chunk)
    return chunks

def most_calories(list):
    return max(sum(x) for x in list)

def top_three_calories(list):
    if len(list) < 3:
        return None
    return sum(sorted(sum(x) for x in list)[-3:])

def main():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    chunked = [[int(x) for x in y] for y in chunks(input)]
    print("Elf with most calories:")
    print(most_calories(chunked))
    print("Elves with top three calories:")
    print(top_three_calories(chunked))

if __name__ == '__main__':
    main()
