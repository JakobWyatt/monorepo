import sys
import pprint

class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.files = []
        self.dirs = {}
    
    def add_file(self, file):
        self.files.append(file)

    def add_dir(self, dir):
        self.dirs[dir.name] = dir

    def print(self, depth):
        prefix = depth * '  '
        midprefix = '\n' + prefix
        filestr = prefix + midprefix.join([repr(x) for x in self.files])
        dirstr = prefix + midprefix.join([x.print(depth + 1) for x in self.dirs.values()])
        return f"dir {self.name}\n{filestr}\n{dirstr}"

    def __str__(self):
        return self.print(1)


class File:
    def __init__(self, name, parent, size):
        self.name = name
        self.size = size
        self.parent = parent

    def __repr__(self):
        return f"file {self.name} size {self.size}"


def create_file_tree(input):
    # default tree position is /
    # must discover directory before entering it
    root = Directory('/', None)
    loc = root
    lsmode = False
    for line in input:
        if line[:4] == '$ cd':
            lsmode = False
            # different cd commands
            if line[5] == '/':
                loc = root
            elif len(line) == 7 and line[5:] == '..':
                loc = loc.parent
            else:
                loc = loc.dirs[line[5:]]
        elif line[:4] == "$ ls":
            lsmode = True
        elif lsmode:
            a, b = line.split(' ')
            if a == 'dir':
                dir = Directory(b, loc)
                loc.add_dir(dir)
            else:
                file = File(b, loc, int(a))
                loc.add_file(file)
        else:
            print("Error parsing.")
            break
    return root


def main():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    root = create_file_tree(input)
    print(root)

if __name__ == "__main__":
    main()
