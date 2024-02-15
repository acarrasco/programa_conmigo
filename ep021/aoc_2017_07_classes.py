from collections import Counter

class Tower:
    def __init__(self, input):
        self._weights = {node: weight for node, weight, _ in input}
        self._children = {node: children for node, _, children in input}
        self._parent = {child: node for node, _, children in input for child in children}
        self._subtree_weights = {}

    def children(self, node):
        return self._children.get(node, [])

    def parent(self, node):
        return self._parent.get(node, None)

    def siblings(self, node):
        all_siblings = self.children(self.parent(node))
        return [sibling for sibling in all_siblings if sibling != node]

    def subtree_weight(self, node):
        if node not in self._subtree_weights:
            own_weight = self.node_weight(node)
            children_weight = sum(self.subtree_weight(child) for child in self.children(node))
            self._subtree_weights[node] = own_weight + children_weight

        return self._subtree_weights[node]

    def node_weight(self, node):
        return self._weights[node]
    
    def is_balanced(self, node):
        children = self.children(node)
        children_weights = set(self.subtree_weight(child) for child in children)
        return len(children_weights) <= 1

def parse_line(line):
    '''
    >>> parse_line('suvtxzq (242) -> tdoxrnb, oanxgk')
    ('suvtxzq', 242, ['tdoxrnb', 'oanxgk'])

    >>> parse_line('smjsfux (7)')
    ('smjsfux', 7, [])
    '''
    line = line.strip()
    if ' -> ' in line:
        left, right = line.split(' -> ')
        children = right.split(', ')
    else:
        left = line
        children = []
    parent, weight = left.split()

    return parent, int(weight[1:-1]), children

def part_1(input):
    all_children = set()
    all_nodes = set()
    for node, _weight, children in input:
        all_nodes.add(node)
        all_children.update(children)

    root, = all_nodes.difference(all_children)
    return root


def find_balance(tower, node, target):
    children = tower.children(node)
    children_weights = list(map(tower.subtree_weight, children))
    weight_counts = Counter(children_weights)

    if len(weight_counts) <= 1: # we need to adjust this node's weight
        return target - sum(children_weights)

    if len(weight_counts) > 2:
        raise 'more than one change needed'

    ((most_common_weight, repetitions),) = weight_counts.most_common(1)

    if repetitions > 1: # there is more than one child with the same weight
        next_target = most_common_weight
        # balance the child that does not share weight with the others
    elif all(map(tower.is_balanced, children)): # two different weights, but they are balanced
        # the target is the one that when duplicated matches the target
        next_target = (target - tower.node_weight(node)) // 2
    else: # two different weights, we have to fix the one that isn't balanced
        balanced_child = next(child for child in tower.children(node) if tower.is_balanced(child))
        next_target = tower.subtree_weight(balanced_child)

    unbalanced_child = next(c for c, w in zip(children, children_weights) if w != next_target)
    return find_balance(tower, unbalanced_child, next_target)

def part_2(root, input):
    tower = Tower(input)
    return find_balance(tower, root, None)

if __name__ == '__main__':
    input = list(map(parse_line, open('input.txt')))
    root = part_1(input)
    print(root)
    new_weight = part_2(root, input)
    print(new_weight)
