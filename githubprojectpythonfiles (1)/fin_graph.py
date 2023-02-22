'''
    1) Build graph using s1 to s3
    2) If graph already exists, draw it using pyplot

    Usage: - fin(org) builds (if not done) and draws a graph
           - If you want to only draw, call drawGraph(G,org) where G=nx.read_gml(path_to_gml,label='label') and org is string 

    Note: It is assumed that if you do not have a GML file,  you will not have structs. Converse is not assumed.
          Thus, if you want to do everything from start, delete all the files for an org in respective folders. 
    #TODO try catch for every function
'''
import networkx as nx
import matplotlib.pyplot as plt
import os
from pprint import pprint 
import requests
import utils.helper_methods as helper_methods
from utils.apiToken import getToken
import time

import s4_fast_userRepoList
import s5_fast_userUserList
import s6_fast_repoRepoList
import s7_enhance_repo

def fin(org):
    start=time.time()
    print(org)
    print("======================================================")
    if not os.path.exists('data/output/gml/'+org+'.gml'):
        remainAtStart = requests.get('https://api.github.com/rate_limit',
                                 headers=helper_methods.seekHeaders()).json()["resources"]["core"]["remaining"]
        try:
            G = buildGraph(org)
            nx.write_gml(G, 'data/output/gml/'+org+'.gml')
            G = nx.read_gml('data/output/gml/'+org+'.gml', label='label')
            drawGraph(G, org)
            print("done for "+org)
            remainAtEnd = requests.get('https://api.github.com/rate_limit',
                                    headers=helper_methods.seekHeaders()).json()["resources"]["core"]["remaining"]
            requestConsumed=remainAtStart-remainAtEnd
            print("Requests consumed -> ",requestConsumed)
            end=time.time()
            stringTimeTaken,timeTaken=helper_methods.elapsed_time(start,end)
            return str("done for "+org), round(timeTaken),requestConsumed
        except Exception as e:
            print(e)
            print("failed for "+org)
            remainAtEnd = requests.get('https://api.github.com/rate_limit',
                                    headers=helper_methods.seekHeaders()).json()["resources"]["core"]["remaining"]
            requestConsumed = remainAtStart- remainAtEnd
            print("Requests consumed -> ", requestConsumed)
            end = time.time()
            stringTimeTaken, timeTaken = helper_methods.elapsed_time(start, end)
            return str("failed for "+org), round(timeTaken), requestConsumed
    else:
        print("already exists for "+org)
        end = time.time()
        stringTimeTaken, timeTaken = helper_methods.elapsed_time(start, end)
        return str("done for "+org), round(timeTaken), 0


def drawGraph(G, org):
    leftNodes = []
    for node in G.nodes():
        if G.nodes[node]['bipartite'] == 0:
            leftNodes.append(node)
    pos = nx.bipartite_layout(G, leftNodes)
    # pos=nx.random_layout(G)

    # draw nodes
    for node in G.nodes():
        if G.nodes[node]['bipartite'] == 0:
            nodeShape = 'o'
            nodeColor = 'lightblue'
        elif G.nodes[node]['bipartite'] == 1:
            nodeShape = 's'
            nodeColor = 'yellow'
        nodelist = [node]
        nx.draw_networkx_nodes(G, pos,
                               node_shape=nodeShape,
                               node_color=nodeColor,
                               node_size=100,
                               nodelist=nodelist)
    # draw edges
    for edge in G.edges():
        edge_color = G.edges[edge]['color']
        edge_style = G.edges[edge]['style']
        # edge_weights=G.edges[edge]['weight']/10
        nx.draw_networkx_edges(G, pos,
                               edgelist=[edge],
                               edge_color=edge_color,
                               style=edge_style)

    # draw labels
    nx.draw_networkx_labels(G, pos,
                            labels={node: node for node in G.nodes()},
                            font_size=8)
    text = f'''
         {org}
         Nodes = {str(len(G.nodes()))}, Edges = {str(len(G.edges()))}
         Users = {str(len(leftNodes))}, Repos = {str(len(G.nodes())-len(leftNodes))}
         Edges: U-R = {str(len([edge for edge in G.edges() if G.edges[edge]['color']=='green']))}, U-U={str(len([edge for edge in G.edges() if G.edges[edge]['color']=='purple']))}, R-R={str(len([edge for edge in G.edges() if G.edges[edge]['color']=='red']))}
         '''
    high, medium, low = 'data/output/plot/a_high/', 'data/output/plot/b_medium/', 'data/output/plot/c_low/'
    path = 'data/output/plot/tooSmallToConsider/'
    if len(G.edges())>=1000:
        path=high
    elif len(G.edges())>=100 and len(G.edges())<1000:
        path=medium
    elif len(G.edges())>=10 and len(G.edges())<100:
        path=low
    plt.title(text)
    plt.gcf().set_size_inches(12, 16)
    plt.savefig(path+org+'.png', dpi=500, bbox_inches='tight')
    plt.clf()


def buildGraph(org):
    G = nx.Graph()
    userRepoEL, users, repos,userStruct, repoStruct = s4_fast_userRepoList.getUserRepoEL(org)
    userUserEL = s5_fast_userUserList.getUserUserEL(org)
    repoRepoEL, edgeWeights = s6_fast_repoRepoList.getRepoRepoEL(org)
    G = addNodes(G, users, repos, userStruct, repoStruct)
    G = addUserRepoEdges(G, userRepoEL)
    G = addUserUserEdges(G, userUserEL)
    G = addRepoRepoEdges(G, repoRepoEL, edgeWeights)
    return G


def addNodes(G, users, repos, userStruct, repoStruct):
    G.add_nodes_from(users, bipartite=0,type="user")
    G.add_nodes_from(repos, bipartite=1,type="repo")
    for user in users:
        if(len(userStruct[user]["languages"]) > 0):
            nx.set_node_attributes(G, {user:userStruct[user]["languages"]}, "languages")
        else:
            nx.set_node_attributes(G, {user:"None"}, "languages")
        if(len(userStruct[user]["topics"]) > 0):
            nx.set_node_attributes(G, {user:userStruct[user]["topics"]}, "topics")
        else:
            nx.set_node_attributes(G, {user:"None"}, "topics")
    for repo in repos:
        try:
            repo_details = s7_enhance_repo.get_repo_details_from_file(
                org="10up", repo=repo)
            nx.set_node_attributes(G, {repo: repo_details["Creation Date"]}, "creation_date")
            if(len(repo_details["Stargazers"]) > 0):
                nx.set_node_attributes(G, {repo: repo_details["Stargazers"]}, "stargazers")
            else:
                nx.set_node_attributes(G, {repo: "None"}, "stargazers")
            if(len(repo_details["Watchers"]) > 0):
                nx.set_node_attributes(G, {repo: repo_details["Watchers"]}, "watchers")
            else:
                nx.set_node_attributes(G, {repo: "None"}, "watchers")
            nx.set_node_attributes(G, {repo: repo_details["Forks Count"]}, "forks_count")
            nx.set_node_attributes(G, {repo: repo_details["Commit Count"]}, "commit_count")
            if(len(repo_details["Topics"]) > 0):
                nx.set_node_attributes(G, {repo:repo_details["Topics"]}, "topics")
            else:
                nx.set_node_attributes(G, {repo:"None"}, "topics")
            if(len(repo_details["Languages"]) > 0):
                nx.set_node_attributes(
                    G, {repo: repo_details["Languages"]}, "languages")
            else:
                nx.set_node_attributes(G, {repo: "None"}, "languages")
        except:
            pass
    return G


def addUserRepoEdges(G, userRepoEL):
    G.add_edges_from(userRepoEL, type='userRepoContribution',
                     color='green', style='solid', weight=100)
    return G


def addUserUserEdges(G, userUserEL):
    G.add_edges_from(userUserEL, type='collaboratedUser',
                     color='purple', style='solid', weight=100)
    return G


def addRepoRepoEdges(G, repoRepoEL, edgeWeights):
    for repoPair in range(len(repoRepoEL)):
        G.add_edge(repoRepoEL[repoPair][0], repoRepoEL[repoPair][1], type='familyRepo',
                   color='red', style='solid', weight=edgeWeights[repoPair])
    # G.add_edges_from(repoRepoEL, type='familyRepo', color='red',style='solid')
    return G

def resetForOrg(org):
    try:
        os.remove('data/output/repoStruct/'+org+'.json')
    except: 
        pass
    try:
        os.remove('data/output/userStruct/'+org+'.json')
    except:
        pass
    try:
        os.remove('data/output/gml/'+org+'.gml')
    except:
        pass
    try:
        os.remove('data/output/plot/a_high/'+org+'.png')
    except:
        pass
    try:
        os.remove('data/output/plot/b_medium/'+org+'.png')
    except:
        pass
    try:
        os.remove('data/output/plot/c_low/'+org+'.png')
    except:
        pass
    try:
        os.remove('data/output/plot/tooSmallToConsider/'+org+'.png')
    except:
        pass

# resetForOrg("10gen")
fin("10up")