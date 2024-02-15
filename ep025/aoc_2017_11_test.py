import unittest

from ep025.aoc_2017_11 import *

class HexDistanceTest(unittest.TestCase):
    def test_adjacent_from(self):
        for di, dj in DIRECTIONS.values():
            result = hex_distance((di, dj))
            self.assertEqual(result, 1)

    def test_far_diagonal(self):
        self.assertEqual(hex_distance((1, 1)), 2)
        self.assertEqual(hex_distance((-1, -1)), 2)

    def test_two_steps_same_direction(self):
        for di, dj in DIRECTIONS.values():
            result = hex_distance((2*di, 2*dj))
            self.assertEqual(result, 2)
