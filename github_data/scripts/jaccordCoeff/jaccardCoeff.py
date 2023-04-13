import networkx as nx


G = nx.read_gexf("./github_data/scripts/u2uConnGraph.gexf")


def jaccard_coefficient(graph, node1, node2):
    neighbors1 = set(graph.neighbors(node1))
    neighbors2 = set(graph.neighbors(node2))
    intersection = neighbors1.intersection(neighbors2)
    union = neighbors1.union(neighbors2)
    if len(union) == 0:
        return 0
    return len(intersection) / len(union)


def jaccard_link_prediction(graph):
    predicted_edges = []
    for node1 in graph.nodes():
        for node2 in graph.nodes():
            if node1 == node2 or graph.has_edge(node1, node2):
                continue
            jaccard = jaccard_coefficient(graph, node1, node2)
            predicted_edges.append((node1, node2, jaccard))
    return sorted(predicted_edges, key=lambda x: x[2], reverse=True)

print(jaccard_link_prediction(G))