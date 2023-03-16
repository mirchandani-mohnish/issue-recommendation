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

headers = {"Authorization": "Bearer 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"}




helper_methods.logData("-----------New Compile---------")
dt = datetime.date.today()
helper_methods.logData(str(dt))
helper_methods.logData("Generating Graphs")

'''
Function used to connect users to issues 
-> goes over each record in pulls.json file
-> makes connections from users to issues via pull requests



'''

def connectUserIssues():
    # with open('../data/raw/pulls.json') as f:
    #     data = json.load(f)
    #     # data =  [line for line in f if line.strip()]
    with open("../data/raw/pulls.json", "rb") as f:
        for record in ijson.items(f, "item"):
            # print(record)
            user = record["head"]["user"]
            user_formatted = json.dumps(user, indent = 4)
            # print(user)
            issueUrl = record["issue_url"]
            linkedIssueData = requests.get(str(issueUrl), headers=headers) # one issue 

            # g.add_node(linkedIssueData.json())
            # g.add_node(user)
            # g.add_edge(linkedIssueData.json(), user_formatted )
            
            # repo = record["repo"]["name"]
            # if user not in user_to_repos:
            #     user_to_repos[user] = set()
            # user_to_repos[user].add(repo)
            print(g)
            time.sleep(1)


