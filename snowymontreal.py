from utils.graph_utils import create_adj_dict
from solve_directed import solve_directed
from solve_undirected import solve_undirected_opti
from solve_undirected import solve_undirected
from utils.osmnx_utils import graph_to_nxgraph
from networkx.algorithms.euler import eulerize, eulerian_circuit
from utils.eulerian_utils import is_eulerian_cycle

def solve_fast(is_oriented, num_vertices, edge_list):
    if not edge_list:
        return []

    if not is_oriented:
        nxgraph = graph_to_nxgraph(edge_list)
        nxgraph_eulerian = eulerize(nxgraph)
        cycle = list(eulerian_circuit(nxgraph_eulerian))

        res = [u for u, v in cycle]
        res.append(res[0])
        return res

    adj_dict = create_adj_dict(num_vertices, edge_list, is_oriented)
    return solve_directed(num_vertices, adj_dict)

def solve(is_oriented, num_vertices, edge_list):
    adj_dict = create_adj_dict(num_vertices, edge_list, is_oriented)

    if not is_oriented:
        return solve_undirected_opti(num_vertices, adj_dict, edge_list)
    return solve_directed(num_vertices, adj_dict)
