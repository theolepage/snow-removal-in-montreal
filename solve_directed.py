from scipy.optimize import linear_sum_assignment
from utils.graph_utils import floyd_warshall, is_edge_in_subgraph_directed, retrieve_path_directed
from utils.eulerian_utils import find_eulerian_cycle_directed, find_already_eulerian_cycle_directed

def get_unbalanced_vertices(adj_dict):
    """
        Compute the degrees of nodes for a directed graph
    """
    dico = {src : 0 for src in adj_dict}
    for src in adj_dict:
        for dst, w in adj_dict[src]:
            dico[src] += 1
            dico[dst] -= 1

    neg, pos, vertices = [], [], []
    for u in dico:
        if dico[u] != 0:
            vertices.append(u)
            if dico[u] > 0:
                pos.extend([u for i in range(dico[u])])
            elif dico[u] < 0:
                neg.extend([u for i in range(abs(dico[u]))])

    return neg, pos, vertices

def solve_directed(num_vertices, adj_dict):
    """
        Change the graph to make it an eulerian graph containing
        an eulerian cycle

        param: num_vertices, the number of vertices in the graph
        param: adj_dict, the adjacency dictionary corresponding to the graph
        return: the eulerian cycle found on the eulerized graph
    """
    if num_vertices == 0:
        return []

    dist, predecessors = floyd_warshall(adj_dict, True)
    for key in dist:
        for val in dist[key]:
            if float("Inf") == dist[key][val]:
                return []

    neg, pos, vertices = get_unbalanced_vertices(adj_dict)
    if not neg:
        return find_already_eulerian_cycle_directed(adj_dict)

    # Create bipartite graph
    bipartite_graph = [[0 for u in pos] for i in neg]
    i = 0
    j = 0
    for src in neg:
        for dst in pos:
            bipartite_graph[i][j] = dist[src][dst]
            j += 1
        j = 0
        i += 1

    # Hungarian method
    rows, cols = linear_sum_assignment(bipartite_graph)
    edges = []
    for i in range(len(rows)):
        edges.append((neg[i], pos[cols[i]]))

    # Put back edges in graph
    for edge in edges:
        weight = dist[edge[0]][edge[1]]
        adj_dict[edge[0]].append((edge[1], weight))

    cycle = find_eulerian_cycle_directed(adj_dict)

    res = [cycle[0][0]]
    for edge in cycle:
        if is_edge_in_subgraph_directed(edge, vertices, dist):
            path = retrieve_path_directed(edge, predecessors)
            for vertex in path:
                res.append(vertex)
        else:
            res.append(edge[1])
    return res
