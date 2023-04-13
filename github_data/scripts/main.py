import sys
sys.path.append('../')

import time
import utils.helper_methods as helper_methods
import github_data.scripts.dataCollection.users as users
import github_data.scripts.dataCollection.issues as issues
import datetime
import json
import threading
import github_data.scripts.dataCollection.pulls as pulls
import pandas as pd
import ijson
import requests 
import networkx as nx
import matplotlib.pyplot as plt
import generateGraph
import github_data.scripts.graphFormation.fileDefinitions as fd

headers = {"Authorization": ""}


helper_methods.logData("-----------New Compile---------")
dt = datetime.date.today()
helper_methods.logData(str(dt))
helper_methods.logData("Main Function File Called")


def logUsers(userData):
    helper_methods.logData("Users being fetched")
    json_object = json.dumps(userData, indent=4)
    with open("../data/raw/users.json", "a") as outfile:
        outfile.write(json_object)
    return

def fetchIssueUsersPulls():
    pulls.fetchPullData()


# generateGraph.connectUserIssues("../data/raw/pulls.json")


# # making graph and connecting user nodes and issue nodes 
# g = generateGraph.loadGraphGml("../graphs/graph_v1.gml")
# print(g)
# helper_methods.logData("Graph: " + str(g))
# g = generateGraph.connectUsers(g)
# generateGraph.saveGraph(g,"../graphs/partConnGraph")
# helper_methods.logData("Graph: " + str(g))
# # g = generateGraph.connectIssues(g)
# # helper_methods.logData("Graph: " + str(g))
# print(g)
# generateGraph.saveGraph(g, "../graphs/ConnGraph")

# generateGraph.connectIssues(g)


gph = generateGraph.loadGraphGexf("./ucongraph.gexf")
generateGraph.connectUsers(gph)