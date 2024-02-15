from collections import Counter

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

def subtree_weight(tree, weights, parent):
    return weights[parent] + sum(subtree_weight(tree, weights, child) for child in tree[parent])

def find_balance(tree, weights, parent, target):
    children_weights = [subtree_weight(tree, weights, node) for node in tree[parent]]
    children_weights_counts = Counter(children_weights)
    unbalanced_children = len(children_weights_counts) > 1
    if unbalanced_children:
        (children_target_weight, _), = children_weights_counts.most_common(1)
        unbalanced_child_index = next(i for i, w in enumerate(children_weights) if w != children_target_weight)
        unbalanced_child_name = tree[parent][unbalanced_child_index]
        return find_balance(tree, weights, unbalanced_child_name, children_target_weight)
    else:
        return target - sum(children_weights)
    
def part_2(root, input):
    weights = {node: weight for node, weight, _ in input}
    tree = {node: children for node, _, children in input}
    return find_balance(tree, weights, root, None)

if __name__ == '__main__':
    input = list(map(parse_line, open('input.txt')))
    root = part_1(input)
    print(root)
    new_weight = part_2(root, input)
    print(new_weight)
