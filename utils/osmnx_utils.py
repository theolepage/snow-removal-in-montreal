import osmnx as ox
import networkx as nx

def nxgraph_to_graph(nxgraph):
    return nxgraph.number_of_nodes(), list(nxgraph.edges(data='length'))

def graph_to_nxgraph(edge_list):
    edges = []
    for edge in edge_list:
        edges.append((edge[0], edge[1], {'length': edge[2]}))
    return nx.from_edgelist(edges)

def nxgraph_from_location(location, network_type):
    return ox.graph_from_place(location, network_type='drive')

def graph_from_location(location, network_type):
    return nxgraph_to_graph(nxgraph_from_location(location, network_type))

if __name__ == "__main__":
    # nxgraph_from_location
    network_type = 'drive' # walk, bike, drive_service, all, all_private, none
    location='Le Tronquay, France'
    print('Loading graph:', location)
    nxgraph = nxgraph_from_location(location, network_type)
    ox.plot_graph(nxgraph)
    # test: print(nxgraph.edges(data=True))

    # nxgraph_to_graph
    num_vertices, edge_list = nxgraph_to_graph(nxgraph)
    print(type(edge_list))
    print(len(edge_list))
    print(num_vertices)

    # graph_to_nxgraph
    nxgraph2 = graph_to_nxgraph(edge_list)
    # test: print(nxgraph2.edges(data=True))
