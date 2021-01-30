import unittest
from utils.eulerian_utils import *
from utils.graph_utils import *
from solve_undirected import kruskal

class IsEulerianCycle(unittest.TestCase):
    def test_is_eulerian_cycle_directed_simple(self):
        edges = [(0, 1, 10), (1, 2, 20), (2, 0, 30)]
        cycle = [0, 1, 2, 0]
        self.assertTrue(is_eulerian_cycle_directed(edges, cycle))

    def test_is_eulerian_cycle_directed_negative(self):
        edges = [(0, 1, 10), (1, 2, 20), (2, 0, 30)]
        cycle = [0, 1, 0]
        self.assertFalse(is_eulerian_cycle_directed(edges, cycle))

    def test_is_eulerian_cycle_directed_hard(self):
        edges = [(0, 1, 0), (1, 2, 0), (2, 0, 0), (2, 3, 0), (3, 4, 0),
                 (4, 2, 0), (0, 6, 0), (6, 4, 0), (4, 5, 0), (5, 0, 0)]
        cycle = [0, 6, 4, 5, 0, 1, 2, 3, 4, 2, 0]
        self.assertTrue(is_eulerian_cycle_directed(edges, cycle))

    def test_is_eulerian_cycle_undirected_simple(self):
        edges = [(0, 1, 10), (1, 2, 20), (2, 0, 30)]
        cycle = [0, 1, 2, 0]
        self.assertTrue(is_eulerian_cycle(edges, cycle))

    def test_is_eulerian_cycle_undirected_hard(self):
        edges = [(0,2,0), (2,3,0), (3,0,0), (2,0,0), (2,1,0), (3,1,0), (1,2,0),
                 (3,2,0), (0,1,0), (0,0,0)]
        cycle = [0,3,2,0,0,2,1,2,3,1,0]
        self.assertTrue(is_eulerian_cycle(edges, cycle))

    def test_is_eulerian_cycle_undirected_negative(self):
        edges = [(0,2,0), (2,3,0), (3,0,0), (2,0,0), (2,1,0), (3,1,0), (1,2,0),
                 (3,2,0), (0,1,0)]
        cycle = [0,3,2,0,2,1,2,1,3,0]
        self.assertFalse(is_eulerian_cycle(edges, cycle))

class FindEulerianCycle(unittest.TestCase):
    def test_find_eulerian_cycle_directed_simple(self):
        adj_dict = {
            0: [(1, 10)],
            1: [(2, 20)],
            2: [(0, 30)]
        }
        res = find_eulerian_cycle_directed(adj_dict)
        self.assertEqual(res, [(0, 1, 10), (1, 2, 20), (2, 0, 30)])

class CyclicTest(unittest.TestCase):

    def test_cyclic_true_small(self):
        n = 4
        edges = [(0, 1, 10), (1, 2, 20), (2, 3, 30)]
        adj_dict = create_adj_dict(n, edges, False)
        self.assertTrue(cyclic(adj_dict, (1, 3, 2), 1))

    def test_cyclic_true_pentagone(self):
        n = 5
        edges  = [(10,20,0),(10,30,0),(10,40,0),(10,50,0),(20,30,0),(20,40,0),
                  (20,50,0),(30,40,0),(30,50,0),(40,50,0)]
        adj_dict = create_adj_dict(n, edges, False)
        self.assertTrue(cyclic(adj_dict, (40, 50, 0), 10))

class MinSpanningTreeTest(unittest.TestCase):

    def test_big_spanning_tree(self):
        n = 4
        edges = [(1, 2, 3), (1, 3, 4), (1, 5, 10),(1, 6, 18), (2, 3, 1),
                 (2, 4, 5),(2, 5, 9), (3, 4, 4), (4, 5, 7),(4, 7, 9), (4, 8, 9),
                 (5, 6, 8),(5, 7, 8), (5, 9, 9), (6, 9, 9), (6, 10, 9),
                 (7, 8, 2), (7, 9, 2),(8, 9, 4), (8, 10, 6), (9, 10, 3)]
        sort_edges(edges, 0, len(edges) - 1)
        adj_dict = create_adj_dict(n, edges, False)
        min_span, e = kruskal([1,2,3,4,5,6,7,8,9,10], edges)
        res = {1: [(2, 3)], 2: [(3, 1), (1, 3)], 3: [(2, 1), (4, 4)],
               4: [(3, 4), (5, 7)], 5: [(4, 7), (6, 8), (7, 8)], 6: [(5, 8)],
               7: [(8, 2), (9, 2), (5, 8)], 8: [(7, 2)], 9: [(7, 2), (10, 3)],
               10: [(9, 3)]}
        self.assertEqual(min_span, res)
