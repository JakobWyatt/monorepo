import sys

def main():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()

if __name__ == "__main__":
    main()
