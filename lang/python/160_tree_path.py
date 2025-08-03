# WORKING START
# input format: a-b: 3, a-c: 5, a-d: 8, d-e: 2, d-f: 4, e-g: 1, e-h: 1
# assume: always given the input in this order (unsure if this will help),  no cycles (well defined tree), not a binary tree.
# find: longest path (can move up and down nodes). This means we cannot repeat nodes.

# initial thoughts:
# trees are recursive, perhaps some information about the greatest path so far can be stored at the subtree root?
# subtrees a, b
#  c
# /\
# a b
# for each node we can either:
# Go up greatest path & further, or
# Go up greatest path & down 2nd greatest path
# So each node needs to hold:
# The score if it is the root node for the path
# The score if it is a sub-node for the path
# WORKING END

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Node:
    def __init__(self, name: str, weight: float, nodes: list['Node']):
        self.name = name
        self.weight = weight
        self.nodes = nodes
        # best path if this is descended into, contains name of self
        self.best_path = []

class TreeSolver:
    def __init__(self):
        self.max_weight = None
        self.best_path = []

    def solve_tree(self, root: Node):
        assert(root.weight == 0.0)
        descend_weight = self._solve_node(root)
        if self.max_weight is None or descend_weight > self.max_weight:
            self.best_path = root.best_path
            self.max_weight = descend_weight
        return self.max_weight

    def _solve_node(self, node : Node):
        weights = []
        for subnode in node.nodes:
            weights.append(self._solve_node(subnode))
        i, j = get_largest_2_elems(weights)
        if i is None:
            node.best_path = [node.name]
            return node.weight
        node.best_path = node.nodes[i].best_path + [node.name]
        if j is not None:
            path_length_if_root = weights[i] + weights[j]
            if self.max_weight is None or self.max_weight < path_length_if_root:
                self.max_weight = path_length_if_root
                self.best_path = node.nodes[i].best_path + [node.name] + list(reversed(node.nodes[j].best_path))
                logger.debug(f"updated best path {self.best_path} weight {self.max_weight}")
        return node.weight + weights[i]

def get_largest_2_elems(x):
    if not x:
        return (None, None)
    if len(x) == 1:
        return (0, None)
    # value, index
    top1 = (None, None)
    top2 = (None, None)
    for i, elem in enumerate(x):
        if top1[0] is None:
            top1 = (elem, i)
        elif elem > top1[0]:
            top2 = top1
            top1 = (elem, i)
        elif top2[0] is None:
            top2 = (elem, i)
        elif elem > top2[0]:
            top2 = elem
    return (top1[1], top2[1])

def parse_tree(input: str):
    # input format: a-b: 3, a-c: 5, a-d: 8, d-e: 2, d-f: 4, e-g: 1, e-h: 1
    node_lookup = {}
    root = None
    for node_str in input.split(', '):
        pair, weight = node_str.split(': ')
        top, bottom = pair.split('-')
        if bottom not in node_lookup:
            node_lookup[bottom] = Node(bottom, 0.0, [])
        node_lookup[bottom].weight = float(weight)
        if top not in node_lookup:
            node_lookup[top] = Node(top, 0.0, [])
        node_lookup[top].nodes.append(node_lookup[bottom])
        if root is None:
            root = node_lookup[top]
    return root

if __name__ == '__main__':
    # build example tree, we can parse it from input later
    g = Node('G', 10, [])
    h = Node('H', 1, [])
    e = Node('E', 2, [g, h])
    f = Node('F', 10, [])
    d = Node('D', 8, [e, f])
    b = Node('B', 3, [])
    c = Node('C', 5, [])
    a = Node('A', 0, [d])

    tree = parse_tree('a-b: 3, a-c: 5, a-d: 8, d-e: 2, d-f: 4, e-g: 1, e-h: 1')

    solver = TreeSolver()
    solver.solve_tree(tree)
    print('\nBest path has weight {} ({})'.format(solver.max_weight, ' -> '.join(solver.best_path)))
