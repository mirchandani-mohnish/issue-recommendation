import networkx as nx
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import github_data.scripts.graphFormation.fileDefinitions as fd
import utils.helper_methods as helper_methods
from networkx.algorithms import bipartite
import time
# # create the bipartite graph
# B = nx.Graph()

# # add users
# users = ['User1', 'User2', 'User3', 'User4']
# B.add_nodes_from(users, bipartite=0)

# # add issues
# issues = ['Issue1', 'Issue2', 'Issue3', 'Issue4']
# B.add_nodes_from(issues, bipartite=1)

# # add edges between users and issues via pull requests
# B.add_edges_from([('User1', 'Issue1'), ('User2', 'Issue2'), ('User3', 'Issue3'), ('User4', 'Issue4')])

# # add edges between users via commonly starred repositories
# B.add_edges_from([('User1', 'User2'), ('User2', 'User3'), ('User3', 'User4')])

# # add edges between issues via common languages
# B.add_edges_from([('Issue1', 'Issue2'), ('Issue2', 'Issue3'), ('Issue3', 'Issue4')])

try:
    gph = nx.read_gexf(fd.fullyConnGraphFile)
    helper_methods.logData("graph file found at " + str())
except Exception as e:
    helper_methods.logData(e)
    gph = nx.Graph()
    helper_methods.logData("new graph file generated")





B = gph
# users = []
# issues = []
# for n in B:
#     if(n == 0):
#         users.append(n)
#     else:
#         issues.append(n)
users = [n for n, d in B.nodes(data=True) if d["bipartite"] == 0]
issues = [n for n, d in B.nodes(data=True) if d["bipartite"] == 1]




# create adjacency matrices for the users and issues
users_matrix = nx.bipartite.biadjacency_matrix(B, bipartite=0)
issues_matrix = nx.bipartite.biadjacency_matrix(B, bipartite=1)

# compute the Jaccard coefficient between all pairs of users and issues
jaccard_matrix = np.zeros((len(users), len(issues)))
for u, i in combinations(range(len(users)), 2):
    u_vec = users_matrix[u].toarray()[0]
    i_vec = issues_matrix[i].toarray()[0]
    jaccard = len(set(np.where(u_vec)[0]).intersection(np.where(i_vec)[0])) / len(set(np.where(u_vec)[0]).union(np.where(i_vec)[0]))
    jaccard_matrix[u][i] = jaccard
    jaccard_matrix[i][u] = jaccard

# compute the Adamic-Adar similarity between all pairs of users and issues
aa_matrix = np.zeros((len(users), len(issues)))
for u, i in combinations(range(len(users)), 2):
    u_vec = users_matrix[u].toarray()[0]
    i_vec = issues_matrix[i].toarray()[0]
    common = np.where(np.logical_and(u_vec, i_vec))[0]
    aa = 0
    for c in common:
        aa += 1 / np.log(len(np.where(users_matrix[:, c].toarray())[0]))
    aa_matrix[u][i] = aa
    aa_matrix[i][u] = aa

# print the predicted links based on Jaccard coefficient
jaccard_threshold = 0.5
jaccard_preds = []
for u in users:
    for i in issues:
        if B.has_edge(u, i):
            continue
        if jaccard_matrix[users.index(u)][issues.index(i)] > jaccard_threshold:
            jaccard_preds.append((u, i))
print("Predicted links based on Jaccard coefficient:", jaccard_preds)

# print the predicted links based on Adamic-Adar similarity
aa_threshold = 0.5
aa_preds = []
for u in users:
    for i in issues:
        if B.has_edge(u, i):
            continue
        if aa_matrix[users.index(u)][issues.index(i)] > aa_threshold:
            aa_preds.append((u, i))
print("Predicted links based on Adamic-Adar similarity:", aa_preds)

