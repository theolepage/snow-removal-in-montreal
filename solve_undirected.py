from utils.matching_utils import find_maximum_matching
from utils.eulerian_utils import is_edge_connected, get_odd_vertices, find_eulerian_cycle, find_already_eulerian_cycle
from utils.graph_utils import floyd_warshall, sort_edges, cyclic, is_edge_in_subgraph, retrieve_path
import copy

def kruskal(odd_vertices, edge_list):
    """
        Find the minimal spanning tree of a graph

        param: odd_vertices, the list of the vertex of the graph
        param: edge_list, the dictionnary representing the graph
        return: res, the dictionary that represent the minimum spanning tree
    """
    res = { v:[] for v in odd_vertices }
    edges = []
    for edge in edge_list:
        if not res[edge[0]] or not res[edge[1]]:
            res[edge[0]].append((edge[1], edge[2]))
            res[edge[1]].append((edge[0], edge[2]))
            edges.append(edge)
        elif not cyclic(res, edge, edge[0]):
            res[edge[0]].append((edge[1], edge[2]))
            res[edge[1]].append((edge[0], edge[2]))
            edges.append(edge)
            i = 0
            for vertex in res:
                if not res[vertex]:
                    break
                if is_edge_connected(1, res, edges):
                    return res, edges
    return res, edges

def iteration_matching(odd_vertices, odd_graph_edge_list, edges):
    odd_vertices_copy = copy.deepcopy(odd_vertices)
    for edge in edges:
        i = 0
        while i < len(odd_graph_edge_list):
            odd_edge = odd_graph_edge_list[i]
            if odd_edge[0] == edge[0] or odd_edge[0] == edge[1]:
                odd_graph_edge_list.remove(odd_edge)
            elif odd_edge[1] == edge[0] or odd_edge[1] == edge[1]:
                odd_graph_edge_list.remove(odd_edge)
            else:
                i += 1
        odd_vertices_copy.remove(edge[0])
        odd_vertices_copy.remove(edge[1])

    edges_2 = []
    half_odds = len(odd_vertices) / 2
    while len(edges) != half_odds:
        for edge in edges_2:
            i = 0
            while i < len(odd_graph_edge_list):
                odd_edge = odd_graph_edge_list[i]
                if odd_edge[0] == edge[0] or odd_edge[0] == edge[1]:
                    odd_graph_edge_list.remove(odd_edge)
                elif odd_edge[1] == edge[0] or odd_edge[1] == edge[1]:
                    odd_graph_edge_list.remove(odd_edge)
                else:
                    i += 1
            odd_vertices_copy.remove(edge[0])
            odd_vertices_copy.remove(edge[1])

        # Find minimum spanning tree
        min_spanning_tree, e = kruskal(odd_vertices_copy, odd_graph_edge_list)

        # Apply matching on min_spanning_tree
        edges_2 = find_maximum_matching(len(odd_vertices_copy), min_spanning_tree)
        for edge in edges_2:
            edges.append(edge)
    return edges

def solve_undirected(num_vertices, adj_dict, edge_list):
    """
        Change the graph to make it an eulerian graph containing
        an eulerian cycle

        param: num_vertices, the number of vertices in the graph
        param: adj_dict, the adjacency dictionary corresponding to the graph
        param: edge_list, the list of edges describing the graph
        return: the eulerian cycle found on the eulerized graph
    """
    if num_vertices == 0:
        return []
    if not is_edge_connected(num_vertices, adj_dict, edge_list):
        return []

    odd_vertices = get_odd_vertices(adj_dict)
    if not odd_vertices:
        return find_already_eulerian_cycle(adj_dict, edge_list)

    # Create a sub graph containing odd degree vertices
    odd_graph = { k:[] for k in odd_vertices }
    odd_graph_edge_list = []

    dist, predecessors = floyd_warshall(adj_dict)
    for src in odd_vertices:
        for dst in odd_vertices:
            if src != dst:
                odd_graph[src].append((dst, dist[src][dst]))
                if ((dst, src, dist[dst][src]) not in odd_graph_edge_list):
                    odd_graph_edge_list.append((src, dst, dist[src][dst]))

    sort_edges(odd_graph_edge_list, 0, len(odd_graph_edge_list) - 1)
    # Find minimum spanning tree
    min_spanning_tree, e = kruskal(odd_vertices, odd_graph_edge_list)
    # Apply matching on min_spanning_tree
    edges = find_maximum_matching(len(odd_vertices), min_spanning_tree)

    if len(edges) != len(odd_vertices) / 2:
        edges = iteration_matching(odd_vertices, odd_graph_edge_list, edges)

    # Put back edges in graph
    for edge in edges:
        weight = dist[edge[0]][edge[1]]
        adj_dict[edge[0]].append((edge[1], weight))
        adj_dict[edge[1]].append((edge[0], weight))
        edge_list.append((edge[0], edge[1], weight))

    cycle = find_eulerian_cycle(adj_dict, edge_list)
    res = [cycle[0][0]]
    for edge in cycle:
        if is_edge_in_subgraph(edge, odd_vertices, dist):
            path = retrieve_path(edge, predecessors)
            for vertex in path:
                res.append(vertex)
        else:
            res.append(edge[1])
    return res








def idle_matching(adj_dict, edges, odd_vertices, dist):
    # Double every edge
    len_edges = len(edges)
    for i in range(len_edges):
        edge = edges[i]
        edges.append(edge)
        adj_dict[edge[0]].append((edge[1], edge[2]))
        adj_dict[edge[1]].append((edge[0], edge[2]))
    cycle = find_eulerian_cycle(adj_dict, edges)

    # Create both matching of the cycle created
    matching1, matching2 = [], []
    sum1, sum2 = 0,0
    is_1 = True
    check = { v:False for v in odd_vertices }
    check[cycle[0][0]] = True
    length = len(cycle)
    i = 0
    while i < length:
        edge = cycle[i]
        src = edge[0]
        while check[edge[1]] and i < length - 1:
            i += 1
            edge = cycle[i]
        check[edge[1]] = True
        w = dist[src][edge[1]]
        if is_1:
            matching1.append((src, edge[1], w))
            sum1 += w
        else:
            matching2.append((src, edge[1], w))
            sum2 += w
        is_1 = not is_1
        i += 1
    if sum1 <= sum2:
        return matching1
    return matching2





def solve_undirected_opti(num_vertices, adj_dict, edge_list):
    """
        Change the graph to make it an eulerian graph containing
        an eulerian cycle

        param: num_vertices, the number of vertices in the graph
        param: adj_dict, the adjacency dictionary corresponding to the graph
        param: edge_list, the list of edges describing the graph
        return: the eulerian cycle found on the eulerized graph
    """
    if num_vertices == 0:
        return []
    if not is_edge_connected(num_vertices, adj_dict, edge_list):
        return []

    odd_vertices = get_odd_vertices(adj_dict)
    if not odd_vertices:
        return find_already_eulerian_cycle(adj_dict, edge_list)

    # Create a sub graph containing odd degree vertices
    odd_graph = { k:[] for k in odd_vertices }
    odd_graph_edge_list = []
    dist, predecessors = floyd_warshall(adj_dict)
    for src in odd_vertices:
        for dst in odd_vertices:
            if src != dst:
                odd_graph[src].append((dst, dist[src][dst]))
                if ((dst, src, dist[dst][src]) not in odd_graph_edge_list):
                    odd_graph_edge_list.append((src, dst, dist[src][dst]))

    sort_edges(odd_graph_edge_list, 0, len(odd_graph_edge_list) - 1)
    # Find minimum spanning tree
    min_spanning_tree, edges = kruskal(odd_vertices, odd_graph_edge_list)

    # Apply matching on min_spanning_tree
    edges = idle_matching(min_spanning_tree, edges, odd_vertices, dist)

    # Put back edges in graph
    for edge in edges:
        weight = dist[edge[0]][edge[1]]
        adj_dict[edge[0]].append((edge[1], weight))
        adj_dict[edge[1]].append((edge[0], weight))
        edge_list.append((edge[0], edge[1], weight))

    cycle = find_eulerian_cycle(adj_dict, edge_list)
    res = [cycle[0][0]]
    for edge in cycle:
        if is_edge_in_subgraph(edge, odd_vertices, dist):
            path = retrieve_path(edge, predecessors)
            for vertex in path:
                res.append(vertex)
        else:
            res.append(edge[1])
    return res
