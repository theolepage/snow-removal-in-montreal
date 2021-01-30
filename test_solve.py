import unittest
from snowymontreal import solve
from utils.osmnx_utils import graph_from_location
from utils.eulerian_utils import is_eulerian_cycle_directed
from utils.eulerian_utils import is_eulerian_cycle
import copy

class SolveDirectedTest(unittest.TestCase):
    def test_directed_empty(self):
        n = 0
        edges = []
        res = solve(True, n, edges)
        self.assertEqual([], res)

    def test_directed_small(self):
        n = 7
        edges = [(0, 1, 25), (0, 5, 20), (1, 2, 20), (2, 6, 17), (2, 0, 65536),
                 (3, 0, 10), (3, 4, 30), (4, 6, 3), (5, 3, 18), (5, 4, 42),
                 (6, 5, 50), (0, 7, 3), (7, 5, 10), (0, 7, 4)]
        expected = [0, 7, 5, 3, 0, 1, 2, 0, 7, 5, 3, 0, 5, 4, 6, 5, 3, 4, 6, 5,
                    3, 0, 1, 2, 6, 5, 3, 0]
        res = solve(True, n, edges)
        self.assertEqual(expected, res)

    def test_directed_tronquay(self):
        n, edges = graph_from_location('Le Tronquay, France', 'drive')
        res = solve(True, n, edges)
        self.assertTrue(is_eulerian_cycle_directed(edges, res))

class SolveUndirectedTest(unittest.TestCase):
    def test_undirected_empty(self):
        n = 0
        edges = []
        res = solve(False, n, edges)
        self.assertEqual([], res)

    def test_undirected_small(self):
        n = 4
        edges = [(0, 1, 10), (1, 2, 20), (2, 3, 30), (1, 3, 2)]
        cycle = solve(False, n, edges)
        self.assertEqual(cycle[0], 0)
        self.assertEqual(cycle[1], 1)
        self.assertEqual(cycle[2], 3)
        self.assertEqual(cycle[3], 2)
        self.assertEqual(cycle[4], 1)
        self.assertEqual(cycle[5], 0)

    def test_undirected_pentagone(self):
        n = 5
        edges  = [(10,20,0),(10,30,0),(10,40,0),(10,50,0),(20,30,0),(20,40,0),
                  (20,50,0),(30,40,0),(30,50,0),(40,50,0)]
        cycle = solve(False, n, edges)
        self.assertEqual(cycle[0], 10)
        self.assertEqual(cycle[1], 50)
        self.assertEqual(cycle[2], 40)
        self.assertEqual(cycle[3], 30)
        self.assertEqual(cycle[4], 50)
        self.assertEqual(cycle[5], 20)
        self.assertEqual(cycle[6], 40)
        self.assertEqual(cycle[7], 10)
        self.assertEqual(cycle[8], 30)
        self.assertEqual(cycle[9], 20)
        self.assertEqual(cycle[10],10)

    def test_undirected_hard(self):
        n = 10
        edges = [(1, 2, 3), (1, 3, 4), (1, 5, 10), (1, 6, 18), (2, 3, 1),
                 (2, 4, 5), (2, 5, 9), (3, 4, 4), (4, 5, 7), (4, 7, 9),
                 (4, 8, 9), (5, 6, 8), (5, 7, 8), (5, 9, 9), (6, 9, 9),
                 (6, 10, 9), (7, 8, 2), (7, 9, 2), (8, 9, 4), (8, 10, 6),
                 (9, 10, 3)]
        cycle = solve(False, n, edges)
        res = [1, 6, 10, 9, 10, 8, 9, 7, 8, 4, 7, 5, 9, 6, 5, 4, 3, 4,
               2, 5, 1, 3, 2, 1]
        self.assertEqual(cycle, res)

    def test_undirected_star(self):
        n = 6
        edges  = [(0,1,10),(0,3,10),(0,4,10),(0,5,10),(0,2,10)]
        cycle = solve(False, n, edges)
        res = [0, 2, 0, 5, 0, 4, 0, 3, 0, 1, 0]
        self.assertEqual(cycle, res)

    def test_undirected_star_odd_n(self):
        n = 7
        edges  = [(0,1,10),(0,3,10),(0,4,10),(0,5,10),(0,2,10),(0,6,10)]
        cycle = solve(False, n, edges)
        res = [0, 2, 0, 5, 0, 4, 0, 3, 0, 6, 0, 1, 0]
        self.assertEqual(cycle, res)

    def test_undirected_fractale(self):
        n = 21
        edges  = [(0,1,10),(0,3,10),(0,4,10),(0,5,10),(0,2,10),(1,3,10),(1,6,10),(1,7,10),(1,16,10),(1,2,10),(2,14,10),(2,15,10),(2,20,10),(3,8,10),(3,9,10),(3,17,10),(3,4,10),(4,10,10),(4,11,10),(4,18,10),(5,12,10),(5,13,10),(5,19,10),(4,5,10),(5,2,10)]
        cycle = solve(False, n, copy.deepcopy(edges))
        #res = [0, 1, 6, 1, 16, 1, 7, 1, 2, 5, 13, 5, 12, 5, 19, 5, 2, 20, 2, 15,2, 14, 2, 0, 5, 4, 11, 4, 10, 4, 18, 4, 3, 17, 3, 9, 3, 8, 3, 4,0, 3, 1, 0]
        self.assertTrue(is_eulerian_cycle(edges, cycle))
