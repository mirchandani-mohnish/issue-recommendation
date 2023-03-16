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

from networkx import bipartite

headers = {"Authorization": "Bearer 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"}









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


'''
connectUserIssues(fileName)
params: 
    fileName: relaive or absolute path of file containting pull requests -> .json only
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
            g.add_node(userNodeId,attr=userNodeData, bipartite = 0) # create the first node of bipartite graph 
            g.add_node(issueNodeId, attr=issueNodeData, bipartite = 1) # issue node of graph
            g.add_edge(userNodeId, issueNodeId) # connect both the nodes
            helper_methods.logData("Connection made:" + userNodeId + " --- "+ issueNodeId )
            # helper_methods.logData("Creating Node between" + json.tostring(user) + "and " json.tostring(issueUrl))
            count += 1
            if count >= 20:
                nx.write_gml(g,"../graphs/graph.gml")
                count = 0
            # time.sleep(1)
            time.sleep(0.2)
            print(g)
    return g


def connectUsers(gph):
    helper_methods.logData("---------Connecting Users---------")
    helper_methods
    print("users connected")



def connectIssues(gph):
    print("Issues connected")












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