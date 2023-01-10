import sys
import pprint

class Directory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.files = []
        self.dirs = {}
        self._total_size = None
    
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

    def total_size(self):
        if self._total_size is None:
            self._total_size = sum(x.size for x in self.files) + sum(x.total_size() for x in self.dirs.values())
        return self._total_size

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


def dirs_below_n(root, dirlist):
    n = 100000
    if root.total_size() < n:
        dirlist.append(root)
    for dir in root.dirs.values():
        dirs_below_n(dir, dirlist)
    return dirlist


def find_to_delete(loc, to_free, to_delete):
    if loc.total_size() > to_free and loc.total_size() < to_delete.total_size():
        to_delete = loc
    for dir in loc.dirs.values():
        to_delete = find_to_delete(dir, to_free, to_delete)
    return to_delete


def main():
    with open(sys.argv[1]) as f:
        input = f.read().splitlines()
    root = create_file_tree(input)
    to_free = root.total_size() - (70000000 - 30000000)
    # print(sum(x.total_size() for x in dirs_below_n(root, []))) part 1
    print(find_to_delete(root, to_free, root).total_size())

if __name__ == "__main__":
    main()
