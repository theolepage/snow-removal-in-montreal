def get_next_vertices(i, pos, adj_dict, matching, visited):
    res = []

    # Make sure to alternate between matching and non-matching edges
    if pos % 2 == 1:
        # Determine vertices connected to i and that are not visited
        for edge in matching:
            # Connected to i?
            j = None
            if edge[0] == i:
                j = edge[1]
            elif edge[1] == i:
                j = edge[0]
            else:
                continue

            # Visited?
            if not j in visited:
                res.append(j)
    else:
        for v, w in adj_dict[i]:
            if not v in visited:
                res.append(v)

    return res

def find_augmenting_path_aux(i, pos, visited, adj_dict, matching, free_vertices, path):
    visited.append(i)

    # Stopping case
    if pos != 0 and i in free_vertices:
        return True

    next_vertices = get_next_vertices(i, pos, adj_dict, matching, visited)

    # Stopping case
    if next_vertices == []:
        return False

    # Explore
    for j in next_vertices:
        res = find_augmenting_path_aux(j, pos + 1, visited, adj_dict, matching, free_vertices, path)
        if res:
            path.append(j)
            return True
        visited.remove(j)

def find_augmenting_path(n, adj_dict, matching):
    # Find free vertices
    free_vertices = []
    tmp = []
    for edge in matching:
        tmp.extend([edge[0], edge[1]])
    for v in adj_dict.keys():
        if not v in tmp:
            free_vertices.append(v)

    # Remove matching edges from edges
    new_adj_dict = { v:[] for v in adj_dict.keys() }
    for u in adj_dict.keys():
        for v, w in adj_dict[u]:
            if not (u, v) in matching and not (v, u) in matching:
                new_adj_dict[u].append((v, w))

    # Run algo on each free vertex
    pos = 0
    visited = []
    path = []
    for v in free_vertices:
        res = find_augmenting_path_aux(v, pos, visited, new_adj_dict, matching, free_vertices, path)
        if res:
            path.append(v)
            return path

    return None

def edge_exists(edge, edges):
    edge_r = (edge[1], edge[0])
    for e in edges:
        e_r = (e[1], e[0])
        if e == edge or e_r == edge or e == edge_r or e_r == edge_r:
            return True
    return False

def xor_edges(matching1, matching2):
    res = []
    for edge in matching1:
        if not edge_exists(edge, matching2):
            res.append(edge)
    for edge in matching2:
        if not edge_exists(edge, matching1):
            res.append(edge)
    return res

def path_to_pairs(path):
    res = []
    for p in range(len(path) - 1):
        res.append((path[p], path[p + 1]))
    return res

def find_maximum_matching(num_vertices, adj_dict):
    if num_vertices == 0:
        return []

    M = []
    P = find_augmenting_path(num_vertices, adj_dict, M)
    while P is not None:
        M = xor_edges(M, path_to_pairs(P))
        P = find_augmenting_path(num_vertices, adj_dict, M)
    return M