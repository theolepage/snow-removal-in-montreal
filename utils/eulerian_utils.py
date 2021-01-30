def in_edgelist(edge, edges):
    for e in edges:
        if edge == (e[0], e[1]):
            return True
    return False

def index_of_edge(edge, edges, visited):
    tmp = None
    for i in range(len(edges)):
        if (edges[i][0], edges[i][1]) == edge:
            if visited[i] == 0:
                return i
            tmp = i
    if tmp is not None:
        return tmp
    return -1

def is_eulerian_cycle(edges, cycle):
    if edges == []:
        return True

    visited = [0 for i in edges]
    for i in range(len(cycle) - 1):
        edge = (cycle[i], cycle[i + 1])
        edge_r = (cycle[i + 1], cycle[i])

        index_edge = index_of_edge(edge, edges, visited)
        index_edge_r = index_of_edge(edge_r, edges, visited)

        if index_edge != -1:
            visited[index_edge] += 1
        if index_edge_r != -1:
            visited[index_edge_r] += 1
        if index_edge == -1 and index_edge_r == -1:
            return False
    return not (0 in visited)




def is_eulerian_cycle_directed(edges, cycle):
    if edges == []:
        return True

    visited = []
    for i in range(len(cycle) - 1):
        edge = (cycle[i], cycle[i + 1])

        if in_edgelist(edge, edges):
            if not in_edgelist(edge, visited):
                visited.append(edge)
        else:
            return False

    return len(edges) == len(visited)



def get_odd_vertices(adj_dict):
    """
        Get a list of all vertices of odd degree
    """
    return [i for i in adj_dict.keys() if len(adj_dict[i]) % 2]



def is_edge_connected_dfs(adj_dict, vertex, edges, check, check_edges):
    """
        Auxiliary function of is_edge_connected that makes the dfs
    """
    check[vertex] = True
    length = len(edges)
    for vert, weigth in adj_dict[vertex]:
        for i in range(length):
            a, b, c = edges[i]
            if (a == vertex and b == vert and c == weigth):
                check_edges[i] = True
            elif (a == vert and b == vertex and c == weigth):
                check_edges[i] = True
        if not check[vert]:
            is_edge_connected_dfs(adj_dict, vert, edges, check, check_edges)

def is_edge_connected(num_vertices, adj_dict, edges):
    """
        Check if the graph is connected
    """
    if not num_vertices or not adj_dict:
        return True
    check = { i:False for i in adj_dict.keys() }
    check_edges = [False for _ in range(len(edges))]
    first_vertex = list(adj_dict.keys())[0]
    is_edge_connected_dfs(adj_dict, first_vertex, edges, check, check_edges)
    return not False in check_edges



def search_pos(start, end, edges, checked):
    pos = 0
    for edge in edges:
        if edge == (start, end[0], end[1]) or edge == (end[0], start, end[1]):
            if not checked[pos]:
                return pos
        pos += 1
    return -1

def dfs(i, adj_dict, edges, checked, cycle, start):
    """
        Auxiliary function for find_eulerian_cycle doing a dfs, changes inplace
        the array cycle

        param: i, the current vertex being visited
        param: adj_dict, the dictionary that corresponds to the graph
        param: edges, the edges describing the graph
        param: checked, the array corresponding to whether an edges has already
               been visited
        param: cycle, the list of edges describing the eulerian cycle
        param: start, the starting vertex of the cycle
        return: True, an eulerian cycle has been found in the graph
        return: False, an eulerian cyle has not been found in the graph
    """
    for vertex in adj_dict[i]:
        pos = search_pos(i, vertex, edges, checked)
        if pos != -1:
            checked[pos] = True
            if vertex[0] == start and not (False in checked):
                cycle.append((vertex[0], i, vertex[1]))
                return True
            if dfs(vertex[0], adj_dict, edges, checked, cycle, start):
                cycle.append((vertex[0], i, vertex[1]))
                return True
            checked[pos] = False
    return False

def find_eulerian_cycle(adj_dict, edges):
    """
        Find the eulerian cycle for a graph that has been eulerized

        param: adj_dict, the dictionary representing the graph
        param: edges, the set of edges  of the graph
        return: a list of edge used to describe the eulerian cycle found
    """
    if not adj_dict:
        return []

    checked = [False] * len(edges)
    list_keys = list(adj_dict.keys())
    for i in list_keys: # the first time will return true anyway
        cycle = []
        if dfs(i, adj_dict, edges, checked, cycle, i):
            return cycle
    return cycle

def find_eulerian_cycle_directed(adj_dict):
    if not adj_dict:
        return []

    first_vertex = list(adj_dict.keys())[0]
    current_path = [(first_vertex, -1)]
    res = []
    last_edge = None

    while current_path:
        u_data = current_path[-1]
        u = u_data[0]

        if adj_dict[u]:
            v = adj_dict[u].pop()
            current_path.append(v)
        else:
            v = current_path.pop()
            if last_edge:
                res.append((v[0], last_edge[0], last_edge[1]))
            last_edge = v

    res.reverse()
    return res

def find_already_eulerian_cycle_directed(adj_dict):
    if not adj_dict:
        return []

    first_vertex = list(adj_dict.keys())[0]
    current_path = [first_vertex]
    res = []

    while current_path:
        u = current_path[-1]

        if adj_dict[u]:
            v = adj_dict[u].pop()[0]
            current_path.append(v)
        else:
            v = current_path.pop()
            res.append(v)

    res.reverse()
    return res

def dfs_eulerian(i, adj_dict, edges, checked, cycle, start):
    """
        Auxiliary function for find_already_eulerian_cycle doing a dfs, changes
        inplace the array cycle

        param: i, the current vertex being visited
        param: adj_dict, the dictionary that corresponds to the graph
        param: edges, the edges describing the graph
        param: checked, the array corresponding to whether an edges has already
               been visited
        param: cycle, the list of edges describing the eulerian cycle
        param: start, the starting vertex of the cycle
        return: True, an eulerian cycle has been found in the graph
        return: False, an eulerian cyle has not been found in the graph
    """
    for vertex in adj_dict[i]:
        pos = search_pos(i, vertex, edges, checked)
        if pos != -1:
            checked[pos] = True
            if vertex[0] == start and not (False in checked):
                cycle.append(i)
                return True
            if dfs_eulerian(vertex[0], adj_dict, edges, checked, cycle, start):
                cycle.append(i)
                return True
            checked[pos] = False
    return False

def find_already_eulerian_cycle(adj_dict, edges):
    """
        Find the eulerian cycle for a graph that is originally eulerized

        param: adj_dict, the dictionary representing the graph
        param: edges, the set of edges  of the graph
        return: a list of edge used to describe the eulerian cycle found
    """
    if not adj_dict:
        return []

    checked = [False] * len(edges)
    list_keys = list(adj_dict.keys())
    for i in list_keys: # the first time will return true anyway
        cycle = [i]
        if dfs_eulerian(i, adj_dict, edges, checked, cycle, i):
            return cycle
    return cycle
