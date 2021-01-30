import copy

def create_adj_dict(num_vertices, edge_list, oriented):
    """
        Create the adjacency dictionnary corresponding to the graph

        param: num_vertices, the number of vertices in the graph
        param: edge_list, the list of edges in the graph
        return: node_labels, the dictionnary corresponding to the graph
   """
    node_labels = {}
    for edge in edge_list:
        if not edge[0] in node_labels.keys():
            node_labels[edge[0]] = [(edge[1], edge[2])]
        else:
            node_labels[edge[0]].append((edge[1], edge[2]))

        if not oriented:
            if not edge[1] in node_labels.keys():
                node_labels[edge[1]] = [(edge[0], edge[2])]
            else:
                node_labels[edge[1]].append((edge[0], edge[2]))
    return node_labels



def bellman_ford(adj_dict, src):
    """
        Compute the distance from a src vertex to every other vertex in the
        graph

        param: adj_dict, the dictionnary that represent the graph
        param: src, the vertex from which to compute all the distances
        return: (dist, predecessors),
                    dist, the dictionnary of dictionnary of int that represents
                          the minimum distance between each couple of vertices
                    predecessors, list of predecessors for each vertex for
                          each source
    """
    dist = {v : float("Inf") for v in adj_dict.keys()}
    dist[src] = 0
    predecessor = {v : float("Inf") for v in adj_dict.keys()}

    for v in adj_dict.keys():
        for e in adj_dict[v]:
            a = v
            b = e[0]
            w = e[1]
            if dist[a] != float("Inf") and dist[a] + w < dist[b]:
                predecessor[b] = a
                dist[b] = dist[a] + w
            elif dist[b] != float("Inf") and dist[b] + w < dist[a]:
                predecessor[a] = b
                dist[a] = dist[b] + w

    for v in adj_dict.keys():
        for e in adj_dict[v]:
            if dist[v] != float("Inf") and dist[e[0]] + w < dist[e[0]]:
                return None
    return dist, predecessor



def floyd_warshall(adj_dict, directed = False):
    """
        The function that computes all the minimum distances from n sources to
        n destinations

        param: adj_dict, the dictionnary that represents the graph
        param: directed, boolean specifying of the graph is directed
        return: (dist, predecessors),
                    dist, the dictionnary of dictionnary of int that represents
                          the minimum distance between each couple of vertices
                    predecessors, list of predecessors for each vertex for
                          each source
    """
    dist = {v : {u : float("Inf") for u in adj_dict.keys()} for v in adj_dict.keys()}
    predecessors = {v : {u : v for u in adj_dict.keys()} for v in adj_dict.keys()}

    keys = adj_dict.keys()

    for src in keys:
        dist[src][src] = 0

    if directed:
        for src in keys:
            for e in adj_dict[src]:
                dst = e[0]
                weight = e[1]
                dist[src][dst] = weight
    else:
        for src in keys:
            for e in adj_dict[src]:
                dst = e[0]
                weight = e[1]
                dist[src][dst] = weight
                dist[dst][src] = weight

    for en_passant in keys:
        for src in keys:
            for dst in keys:
                en_passant_length = dist[src][en_passant] + dist[en_passant][dst]
                if en_passant_length < dist[src][dst]:
                    dist[src][dst] = en_passant_length
                    predecessors[src][dst] = predecessors[en_passant][dst]
    return dist, predecessors


def is_edge_in_subgraph(edge, odd_vertices, dist):
    """
        Test if this edge has been added to the graph

        param: edge, the edge to check
        param: odd_vertices, all the vertices of the subgraph
        param: dist, a dictionary of dictionary of int representing the
               minimum distances between two vertices
        return: True, if the edge has been added to the graph
        return: False, if the edge was in the graph at the origin
    """
    is_in = 0
    for vertex in odd_vertices:
        if edge[0] == vertex or edge[1] == vertex:
            if edge[2] == dist[edge[0]][edge[1]]:
                is_in += 1
        if is_in == 2:
            return True
    return False



def is_edge_in_subgraph_directed(edge, vertices, dist):
    """
        Test if this edge has been added to the graph

        param: edge, the edge to check
        param: vertices, all the vertices of the subgraph
        param: dist, a dictionary of dictionary of int representing the
               minimum distances between two vertices
        return: True, if the edge has been added to the graph
        return: False, if the edge was in the graph at the origin
    """
    is_in = 0
    for vertex in vertices:
        if edge[0] == vertex:
            if edge[2] == dist[edge[0]][edge[1]]:
                is_in += 1
        elif edge[1] == vertex:
            if edge[2] == dist[edge[0]][edge[1]]:
                is_in += 1
        if is_in == 2:
            return True
    return False



def retrieve_path(edge, predecessors):
    """
        Find the path between the two vertices of edge

        param: edge, the edge to retrieve the path from
        param: predecessors, the dictionary of predecessors
        return: path, a list representing the path between the two vertices
    """
    curr = edge[0]
    path = []
    pred = predecessors[edge[1]][curr]
    while pred != edge[1]:
        path.append(pred)
        curr = pred
        pred = predecessors[edge[1]][curr]
    path.append(pred)
    return path



def retrieve_path_directed(edge, predecessors):
    """
        Find the path between the two vertices of edge

        param: edge, the edge to retrieve the path from
        param: predecessors, the dictionary of predecessors
        return: path, a list representing the path between the two vertices
    """
    curr = edge[1]
    path = [edge[1]]
    pred = predecessors[edge[0]][curr]
    while pred != edge[0]:
        path.append(pred)
        curr = pred
        pred = predecessors[edge[0]][curr]
    path.reverse()
    return path



def cyclic_aux(v, adj_dict, visited, parent):
    """
        The auxiliary for the cyclic function

        param: v, the current vertex
        param: adj_dic, the representation of the graph in dictionnary
        param: visited, an array of boolean keeping track of the vertices
               already visited
        param: parent, the vertex that led to v
        return: True, a cycle has been found
        return: False, no cycle has been found
    """
    visited[v] = True
    for edge in adj_dict[v]:
        if not visited[edge[0]]:
            if cyclic_aux(edge[0], adj_dict, visited, v):
                return True
        elif parent != edge[0]:
            return True
    return False

def cyclic(adj_dict, edge, start):
    """
        Test if there is a cycle in the graph once the "edge" edge added

        param: adj_dict, the dictionnary representing the graph
        param: edge, the edge to add before testing
        param: start, the vertex from where to start the research for a cycle
        return: True, if the graph contains a cycle
        return: False, if the graph does not contains a cycle
    """
    # Add edge to graph
    adj_dict_copy = copy.deepcopy(adj_dict)
    adj_dict_copy[edge[0]].append((edge[1], edge[2]))
    adj_dict_copy[edge[1]].append((edge[0], edge[2]))

    visited = { v:False for v in adj_dict_copy.keys() }
    for src in adj_dict.keys():
        if not visited[src]:
            if cyclic_aux(src, adj_dict_copy, visited, -1):
                return True
    return False



def sort_edges_aux(edge_list, low, high):
    """
        The auxiliary funtion of quik sort

        param: edge_list, the edge list to sort
        param: low, the index of the smallest edge
        param: high, the index of the biggest edge
        return: the index of the new pivot
    """
    i = low - 1
    pivot = edge_list[high]

    for j in range(low, high):
        if edge_list[j][2] <= pivot[2]:
            i += 1
            edge_list[i], edge_list[j] = edge_list[j], edge_list[i]

    edge_list[i + 1], edge_list[high] = edge_list[high], edge_list[i + 1]
    return i + 1

def sort_edges(edge_list, low, high):
    """
        Sort an edge list inplace from the smallest weigth to the bigest one
        with a quick sort

        param: edge_list, the list of all the edges to sort
        param: low, the index of the smallest edge
        param: high, the index of the biggest edge
    """
    if low < high:
        pi = sort_edges_aux(edge_list, low, high)
        sort_edges(edge_list, low, pi - 1)
        sort_edges(edge_list, pi + 1, high)