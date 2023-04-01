import networkx as nx
import math

G = nx.read_gexf("./github_data/scripts/u2uConnGraph.gexf")

def adamic_adar_coefficient(graph, node1, node2):
    neighbors1 = set(graph.neighbors(node1))
    neighbors2 = set(graph.neighbors(node2))
    common_neighbors = neighbors1.intersection(neighbors2)
    aa = sum([1 / math.log(len(set(graph.neighbors(neighbor)))) for neighbor in common_neighbors])
    return aa

def adamic_adar_link_prediction(graph):
    predicted_edges = []
    for node1 in graph.nodes():
        for node2 in graph.nodes():
            if node1 == node2 or graph.has_edge(node1, node2):
                continue
            aa = adamic_adar_coefficient(graph, node1, node2)
            predicted_edges.append((node1, node2, aa))
    return sorted(predicted_edges, key=lambda x: x[2], reverse=True)