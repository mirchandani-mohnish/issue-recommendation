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
import generateGraph
import fileDefinitions as fd

headers = {"Authorization": "Bearer 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"}


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