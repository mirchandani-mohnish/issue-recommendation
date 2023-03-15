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

def fetchUsersViaOrgs():
    orgList = []

    with open("../data/raw/orgs.json", "r") as infile:
        for line in infile:
            line.strip()
            orgList.append(str(line).strip())
        

    helper_methods.logData("Done Reading Org List")

    for org in orgList:
        print(org)
        userData = users.getUsers(org)
        print(userData)
        # logUsers(userData)
        time.sleep(1)


def fetchIssueUsersPulls():
    pulls.fetchPullData()


def connectUserIssues():
    # with open('../data/raw/pulls.json') as f:
    #     data = json.load(f)
    #     # data =  [line for line in f if line.strip()]
    with open("../data/raw/pulls.json", "rb") as f:
        for record in ijson.items(f, "item"):
            # print(record)
            user = record["head"]["user"]
            
            # print(user)
            issueUrl = record["issue_url"]
            linkedIssueData = requests.get(str(issueUrl), headers=headers) # one issue 
            
            # repo = record["repo"]["name"]
            # if user not in user_to_repos:
            #     user_to_repos[user] = set()
            # user_to_repos[user].add(repo)
            time.sleep(0.2)

    # print(data[0])

connectUserIssues()