
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
import fileDefinitions as fd
from dotenv import load_dotenv
import generateGraph as gg



load_dotenv()
headers = {"Authorization": "Bearer " + os.getenv('ACCESS_TOKEN')}

path = "/github_data/graphs"



def connectIssueToIssue(filename):
    helper_methods.logData("Connectig Issues ")
    try:
        with open(fd.issueLogFile, "r") as file:
            lastIssue = json.load(file.read())
    except Exception as e:
        helper_methods.logData(e)
    
    try:
        with open(fd.issueToLangFile, "r") as file:
            issueToLang = json.dump(file.read())
    except Exception as e:
        helper_methods.logData(e)
        issueToLang = {}
        
    try:
         with open(filename, "r") as file:
             gph = loadGraphGexf(filename)  
    except:
        helper_methods.logData("Unable to open graph")
    
    
    for n in gph.nodes(data=True):
        if (lastIssue.length() == 0 or n[0] == lastIssue['id']):
            print(n[0])
            print(n)
            if n[1]['bipartite'] == 1:
                parentRepoUrl = n[1]['attr']['repository_url']
                parentRepoUrl = parentRepoUrl.strip("{/owner}{/repo}")
                # try:
                helper_methods.logData("connecting Issues: " + n[0])
                
                listOfLanguagesUrl = str(parentRepoUrl + "/languages")
                listOfLanguages = requests.get(listOfLanguagesUrl, headers=headers).json()
                for item in listOfLanguages:
                    lang = item[0]
                    if lang != None and lang in issueToLang:
                        issueToLang[lang].append(str(n[0]))
                        for issue in issueToLang[lang]:
                            gph.add_edge(issue,n)
                    else:
                        issueToLang[lang] = [str(n[0]),]
                    print(n[0])
                
                        