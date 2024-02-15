import unittest
from aoc_2017_07_classes import *


def parse_raw_input(raw_input):
    return [parse_line(line) for line in raw_input.splitlines() if line.strip()]

class TowerTest(unittest.TestCase):
    def test_constructor_children(self):
        input = parse_raw_input('''
        root (10) -> a, b
        a (5)
        b (3)''')
        tower = Tower(input)
        expected = {
            'root': ['a', 'b'],
            'a': [],
            'b': []
        }
        self.assertEqual(tower._children, expected)

    def test_children(self):
        input = parse_raw_input('''
        root (10) -> a, b
        a (5)
        b (3)''')
        tower = Tower(input)
        self.assertEqual(tower.children('root'), ['a', 'b'])
        self.assertEqual(tower.children('a'), [])
        self.assertEqual(tower.children('b'), [])

    def test_parent(self):
        input = parse_raw_input('''
        root (10) -> a, b
        a (5)
        b (3)''')
        tower = Tower(input)
        self.assertEqual(tower.parent('a'), 'root')
        self.assertEqual(tower.parent('b'), 'root')
        self.assertEqual(tower.parent('root'), None)

    def test_siblings(self):
        input = parse_raw_input('''
        root (10) -> a, b
        a (5)
        b (3)''')
        tower = Tower(input)
        self.assertEqual(tower.siblings('a'), ['b'])
        self.assertEqual(tower.siblings('b'), ['a'])
        self.assertEqual(tower.siblings('root'), [])

    def test_subtree_weight(self):
        input = parse_raw_input('''
        root (10) -> a, b
        a (5)
        b (3)''')
        tower = Tower(input)
        self.assertEqual(tower.subtree_weight('root'), 18)
        self.assertEqual(tower.subtree_weight('a'), 5)
        self.assertEqual(tower.subtree_weight('b'), 3)
    
    def test_subtree_weight_complex(self):
        input = parse_raw_input('''
                            pbga (66)
                            xhth (57)
                            ebii (61)
                            havc (66)
                            ktlj (57)
                            fwft (72) -> ktlj, cntj, xhth
                            qoyq (66)
                            padx (45) -> pbga, havc, qoyq
                            tknk (41) -> ugml, padx, fwft
                            jptl (61)
                            ugml (68) -> gyxo, ebii, jptl
                            gyxo (61)
                            cntj (57)
                            ''')
        tower = Tower(input)
        self.assertEqual(tower.subtree_weight('ugml'), 251)
        self.assertEqual(tower.subtree_weight('padx'), 243)
        self.assertEqual(tower.subtree_weight('fwft'), 243)
        self.assertEqual(tower.subtree_weight('tknk'), 41 + 2*243 + 251)

    def test_is_balanced(self):
        input = parse_raw_input('''
                            pbga (66)
                            xhth (57)
                            ebii (61)
                            havc (66)
                            ktlj (57)
                            fwft (72) -> ktlj, cntj, xhth
                            qoyq (66)
                            padx (45) -> pbga, havc, qoyq
                            tknk (41) -> ugml, padx, fwft
                            jptl (61)
                            ugml (68) -> gyxo, ebii, jptl
                            gyxo (61)
                            cntj (57)
                            ''')
        tower = Tower(input)
        self.assertEqual(tower.is_balanced('ugml'), True)
        self.assertEqual(tower.is_balanced('padx'), True)
        self.assertEqual(tower.is_balanced('fwft'), True)
        self.assertEqual(tower.is_balanced('tknk'), False)


class TestFindBalance(unittest.TestCase):
    def test_one_level_unbalanced(self):
        raw_input ='''
        root (10) -> a, b, c
        a (5)
        b (3)
        c (5)
        '''
        input = parse_raw_input(raw_input)
        tower = Tower(input)
        result = find_balance(tower, 'root', None)
        self.assertEqual(result, 5)

    def test_second_level_unbalanced(self):
        r'''
        r ___a
          \__b___d
           \_c   \e
                  \f
        '''
        input = parse_raw_input('''
        r (10) -> a, b, c
        a (5)
        b (2) -> d, e, f
        c (5)
        d (1)
        e (1)
        f (4)
        ''')
        tower = Tower(input)

        result = find_balance(tower, 'r', None)
        self.assertEqual(result, 1)

    def test_first_level_unbalanced(self):
        r'''
        r ___a
          \__b___d
           \_c   \e
                  \f
        '''
        raw_input = '''
        r (10) -> a, b, c
        a (5)
        b (0) -> d, e, f
        c (5)
        d (1)
        e (1)
        f (1)
        '''
        tower = Tower(parse_raw_input(raw_input))

        result = find_balance(tower, 'r', None)
        self.assertEqual(result, 2)


    def test_binary_unbalanced_leaves(self):
        r'''
        (10,
            2(1, 2),
            2(1, 1)
        )
        '''
        raw_input = '''
        r (10) -> a, b
        a (2) -> c, d
        b (2) -> e, f
        c (1)
        d (2)
        e (1)
        f (1)
        '''
        tower = Tower(parse_raw_input(raw_input))

        result = find_balance(tower, 'r', None)
        self.assertEqual(result, 1)


    def test_binary_unbalanced_leaves(self):
        r'''
        (0
            10
                (10, 15)
            20
                (10, 10)
        )
        '''
        raw_input = '''
        r (0) -> a, b
        a (10) -> c, d
        b (20) -> e, f
        c (10)
        d (15)
        e (10)
        f (10)
        '''
        tower = Tower(parse_raw_input(raw_input))

        result = find_balance(tower, 'r', None)
        self.assertEqual(result, 15)



if __name__ == '__main__':
    unittest.main()
