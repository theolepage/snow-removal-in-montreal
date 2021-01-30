import argparse
import osmnx as ox
from snowymontreal import solve
from utils.osmnx_utils import *
from utils.eulerian_utils import is_eulerian_cycle, is_eulerian_cycle_directed
import copy

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--oriented", help="use directed graph", action="store_true")
    parser.add_argument("location", help="location (example: 'Le Tronquay, France')")
    args = parser.parse_args()

    nxgraph = nxgraph_from_location(args.location, 'drive')
    ox.plot_graph(nxgraph)
    n, edges = nxgraph_to_graph(nxgraph)
    res = solve(args.oriented, n, copy.deepcopy(edges))

    print(res)
    if args.oriented:
        print(is_eulerian_cycle_directed(edges, res))
    else:
        print(is_eulerian_cycle(edges, res))
