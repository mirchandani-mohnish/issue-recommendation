import sys
sys.path.append('../')

import time
import utils.helper_methods as helper_methods
import users as users
import issues as issues
import datetime
import json
import threading
import pulls as pulls
import pandas as pd
import ijson
import requests 
import networkx as nx
import matplotlib.pyplot as plt
import ijson
import os
from networkx import bipartite

headers = {"Authorization": "Bearer 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"}
path = "/github_data/graphs"


'''
Function used to connect users to issues 
-> goes over each record in pulls.json file
-> makes connections from users to issues via pull requests
'''

def filterUser(userdata):
    if userdata == None:
        print("Error -> no user data")
        helper_methods.logData("Error -> no user data")
        user = {
            "login": "login",
            "id": "id",
            "node_id": "node_id", 
            "url": "url",
            "followers_url": "followers_url",
            "following_url": "following_url",
            "starred_url": "starred_url",
            "repos_url": "repos_url"
        }
        time.sleep(10)
        return user 
    else:
        user = {
            "login": userdata["login"],
            "id": userdata["id"],
            "node_id": userdata["node_id"], 
            "url": userdata["url"],
            "followers_url": userdata["followers_url"],
            "following_url": userdata["following_url"],
            "starred_url": userdata["starred_url"],
            "repos_url": userdata["repos_url"]
        }
    
    helper_methods.logData("Filtering User: "+ user["login"] )
    return user


def filterIssue(issuedata):
    if issuedata == None:
        helper_methods.logData("Error -> no issue data")
        issue = {
            "url": "url",
            "labels_url": "labels_url",
            "id": "id",
            "title": "title",
            "labels": "labels",
            "number":"number",
            "repository_url": "repository_url",
            "node_id": "node_id"
        }
        time.sleep(10)
        return issue 
    else:
        issue = {
            "url": issuedata["url"],
            "labels_url": issuedata["labels_url"],
            "id": issuedata["id"],
            "title": issuedata["title"],
            "labels": issuedata["labels"],
            "labesl_url": issuedata["labels_url"],
            "number": issuedata["number"],
            "repository_url": issuedata["repository_url"],
            "node_id": issuedata["node_id"]
        }
    helper_methods.logData("Filtering Issue: "+ issue["title"] )
    return issue


def loadGraphGml(fileName):
    gph = nx.read_gml(fileName)
    return gph

def loadGraphGexf(fileName):
    gph = nx.read_gexf(fileName)
    return gph


def saveGraph(gph, fileName):
    nx.write_gml(gph,str(fileName + ".gml"))
    nx.write_gexf(gph,str(fileName + ".gexf"))
    nx.write_graphml(gph,str(fileName + ".xml"))
    nx.write_edgelist(gph,str(fileName + ".txt"))
    helper_methods.logData("Done saving graph")
    
'''
connectUserIssues(fileName)
params: 
    fileName: relative or absolute path of file containting pull requests -> .json only
-> function which connects edges between users and issues
-> the function reads the pulls.json file 
-> each issue is fetched using the issue_url
-> each user is taken from the data in pulls.json itslef
-> both are mapped into a bipartite graph with users having bipartite label = 0 
    and issues having bipartite label = 1



'''

def connectUserIssues(fileName):
    g = nx.Graph()
    helper_methods.logData("connecting users and issues")
    count = 0
    with open(fileName, "rb") as f:
        for record in ijson.items(f, "item"): # open the file -> use ijson to fetch a record instead of a line
            user = record["head"]["user"] # take the user from the record 
            user_formatted = json.dumps(user, indent = 4)
            issueUrl = record["issue_url"] # take the issue url from the record 
            linkedIssueData = requests.get(str(issueUrl), headers=headers) # request github api for issue data 
            userNodeData = filterUser(user) # filter out useless content from the user 
            issueNodeData = filterIssue(linkedIssueData.json()) # filter out useless content from issue
            issueNodeId = linkedIssueData.json()["node_id"] # make a node id -> issue node id is the node_id provided by github
            # print(linkedIssueData.json())
            userNodeId = userNodeData["login"] # user node id is the login id
            try:
                g.add_node(userNodeId,attr=userNodeData, bipartite = 0) # create the first node of bipartite graph 
                g.add_node(issueNodeId, attr=issueNodeData, bipartite = 1) # issue node of graph
                g.add_edge(userNodeId, issueNodeId) # connect both the nodes
                helper_methods.logData("Connection made:" + userNodeId + " --- "+ issueNodeId )
            except:
                helper_methods.logData("Connection rejected")
                pass
            # helper_methods.logData("Creating Node between" + json.tostring(user) + "and " json.tostring(issueUrl))
            count += 1
            print(count)
            if count >= 20:
                try:
                    nx.write_gml(g,"../graphs/graph.gml")
                    count = 0
                except:
                    print("unable to write")
                    pass

                try:
                    nx.write_gexf(g,"../graphs/graph.gexf")
                    count = 0
                except:
                    print("unable to write")
                    pass
            # time.sleep(1)
            time.sleep(0.2)
            print(g)
    return g

'''
connectUsers(gph)
params: gph -> graph

-> the function tries to connect all users using starred repositories as an edge 
-> we first check the starredUrl in each node
-> we call the starredUrl to get all the repositories starred by the user
-> we store the same in a dictionary along with other users who have the repository starred
-> we make edges across those users


'''
def connectUsers(gph):
    helper_methods.logData("---------Connecting Users---------")
    userToRepo = {}
    temp_dic = {}
    g = gph
    for n in gph.nodes(data=True):
        if n[1]['bipartite'] == 0:
            starredUrl = n[1]['attr']['starred_url']
            starredUrl = starredUrl.strip("{/owner}{/repo}")
            if(starredUrl  == "starred_url"):
                pass
            else:
                helper_methods.logData("currently at: " + n[0]) #logging
                listOfStarredRepos = requests.get(starredUrl, headers = headers)
                listOfStarredRepos = listOfStarredRepos.json()
                helper_methods.logData("fetched starred repos" + starredUrl) #logging
                time.sleep(0.2)
                for repo in listOfStarredRepos:
                    try:
                        tem = repo['name']
                        ans = ""
                        for i in tem:
                            if i == '-':
                                ans = ans + '_'
                            else:
                                ans = ans + i
                    except Exception as e:
                        helper_methods.logData("Error" + str(e))
                        pass
                    # print(ans)
                    if ((ans in temp_dic) and (str(n[0]) not in temp_dic[ans])):
                        temp_dic[ans].append(str(n[0]))
                    else:
                        # print(ans, ans in temp_dic)
                        temp_dic[ans] = [str(n[0]),]
                helper_methods.logData("Created Dictionary")
               
        time.sleep(0.2)
    
    # print(temp_dic)
    for i in temp_dic.keys():
        arr = temp_dic[i]
        sz = len(arr)
        for j in range(0, sz):
            for k in range(j + 1, sz):
                g.add_edge(arr[j], arr[k])
    try:
        saveGraph(g, "userConnGraph")
    except:
        try:
            nx.write_gml(g,"../graphs/userConnGraph.gml")
            count = 0
        except:
            print("unable to write gml")
            pass

        try:
            nx.write_gexf(g,"../graphs/userConnGraph.gexf")
            count = 0
        except:
            print("unable to write gexf")
            pass


    return g


'''

connectIssues(gph)
params: gph -> graph


-> the function tries to connect all issues using common languages as an edge
-> we get the repository url of parent repo
-> we get the languages url of that repository
-> we fetch all languages
-> for each language, we store the same in a dictionary 
-> then we run over the graph connecting nodes using the edges



'''
def connectIssues(gph):
    helper_methods.logData("---------Connecting Issues---------")
    issueToLang = {}
    count = 0
    for n in gph.nodes(data=True):
        if n[1]['bipartite'] == 1:
            parentRepoUrl = n[1]['attr']['repository_url']
            parentRepoUrl = parentRepoUrl.strip("{/owner}{/repo}")
            # try:
            helper_methods.logData("connecting Issues: " + n[0])
            listOfLanguages = {}
            mostUsedLang = None
            try:
                parentRepoData = requests.get(parentRepoUrl, headers = headers)
                listOfLanguagesUrl = parentRepoData.json()['languages_url']
                listOfLanguages = requests.get(listOfLanguagesUrl, headers=headers).json()
                mostUsedLang = list(listOfLanguages.items())[0][0]
                print(list(listOfLanguages.items())[0][1]) # getting languages 
            except Exception as e:
                print(e)
                helper_methods.logData(e)
                time.sleep(10)

            if mostUsedLang != None:
                if mostUsedLang in issueToLang:
                    issueToLang[mostUsedLang].append(str(n[0]))
                else:
                    issueToLang[mostUsedLang] = [str(n[0]),]
                print(n[0])
            count += 1
            if( count > 20 ):
                with open('../data/misc/issuesToLang.json', 'w') as file:
                    file.write(json.dumps(issueToLang))
                count = 0
            time.sleep(0.2)

    for i in issueToLang.keys():
        arr = issueToLang[i]
        sz = len(arr)
        for j in range(0, sz):
            for k in range(j + 1, sz):
                gph.add_edge(arr[j], arr[k])
                helper_methods.logData("Added edge between" + str(arr[i]) + " and " + str(arr[j]))

    return gph
    # for lang in issueToLang.keys():
    #     for u in lang:
    #         for v in lang:
    #             if(v == u):
    #                 pass
    #             else:
    #                 gph.add_edge(u,v, language=lang) # add edge with language
    print("Issues connected")



'''
generateMetrics(gph)
params: gph -> graph

-> we generate all the metrics related to the graph and store the samein the metrics folder in data

'''



# issueToLang[mostUsedLang].append(str(n[0]))
            # except Exception as e:
            #     helper_methods.logData(e)
            #     helper_methods.logData("Some error occured:" + str(n[0]))
            #     pass

# with open('../data/raw/pulls.json') as f:
    #     data = json.load(f)
    #     # data =  [line for line in f if line.strip()]

# linkedIssueData = requests.get(str(issueUrl), headers=headers) # one issue 

            # g.add_node(linkedIssueData.json())
            # g.add_node(user)
            # g.add_edge(linkedIssueData.json(), user_formatted )
            
            # repo = record["repo"]["name"]
            # if user not in user_to_repos:
            #     user_to_repos[user] = set()
            # user_to_repos[user].add(repo)


# ------ graph connections need to be made here ------
        
            # for lang in listOfLanguages:
            #     if(issueToLang[lang]):
            #         issueToLang[lang].append(n[0])
            #         for us in issueToLang:
            #             nx.set_node_attributes(gph, {}) # dictionary ka locha hai karna hai solve
            #     else:
            #         issueToLang[lang] = []
            #         issueToLang[lang].append(n[0])
            # helper_methods.logData("edges made for node" + n[0])   
        
        # time.sleep(1)