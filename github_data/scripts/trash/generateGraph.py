import sys
sys.path.append('../')

import time
import utils.helper_methods as helper_methods
# import github_data.scripts.dataCollection.users as users
# import github_data.scripts.dataCollection.issues as issues
# import datetime
import json
# import threading
# import github_data.scripts.dataCollection.pulls as pulls
import pandas as pd
import ijson
import requests 
import networkx as nx
import matplotlib.pyplot as plt
import ijson
import os
from networkx import bipartite
import scripts.graphFormation.fileDefinitions as fd
from dotenv import load_dotenv

load_dotenv()
headers = {"Authorization": "Bearer " + os.getenv('ACCESS_TOKEN')}

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
    

def updateConnectLogs(repoName: str,pullCount: int,userData: str,issueData: str):
    connectLogData = {
        "lastRepo": repoName,
        "pullCount": pullCount,
        "lastUser": userData,
        "lastIssue": issueData
    }

    with open(fd.connectLogFile, "w") as file:
        file.write(json.dumps(connectLogData, indent=4))
    
    return True





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


def connectUserIssues(fileName: str):
    try:
        g = loadGraphGexf(fileName)
        helper_methods.logData("graph file found at " + str(fileName))
    except Exception as e:
        helper_methods.logData(e)
        g = nx.Graph()
        helper_methods.logData("new graph file generated")
    
    helper_methods.logData("------Current Graph -------")
    helper_methods.logData(g)

    with open(fd.connectLogFile, "r") as file:
        lastPullData = json.load(file)
    

    helper_methods.logData("connecting users and issues")
    count = 0
    lastPullCount = int(lastPullData['pullCount'])
    updatedLastPullCount = lastPullCount
    with open(fd.pullsFile, "rb") as f:
        for record in ijson.items(f, "item"): # open the file -> use ijson to fetch a record instead of a line
            if(lastPullCount != 0):
                lastPullCount -= 1
                helper_methods.logData("Retreiving predone content: count -> " + str(lastPullCount))
            else:
                try:
                    user = record["head"]["user"] # take the user from the record 
                    user_formatted = json.dumps(user, indent = 4)
                    issueUrl = record["issue_url"] # take the issue url from the record 
                    linkedIssueData = requests.get(str(issueUrl), headers=headers) # request github api for issue data 
                    userNodeData = filterUser(user) # filter out useless content from the user 
                    issueNodeData = filterIssue(linkedIssueData.json()) # filter out useless content from issue
                    # issueNodeId = linkedIssueData.json()["node_id"] # make a node id -> issue node id is the node_id provided by github
                    issueNodeId = issueUrl.split("https://api.github.com/repos/")[1]
                    
                    # print(linkedIssueData.json())
                    userNodeId = userNodeData["login"] # user node id is the login id
                    try:
                        if(g.has_node(userNodeId) == False):
                            g.add_node(userNodeId,attr=userNodeData, bipartite = 0) # create the first node of bipartite graph 
                        if(g.has_node(issueNodeId) == False):
                            g.add_node(issueNodeId, attr=issueNodeData, bipartite = 1) # issue node of graph
                        if(g.has_edge(userNodeId, issueNodeId) == False):    
                            g.add_edge(userNodeId, issueNodeId) # connect both the nodes
                        helper_methods.logData("Connection made:" + userNodeId + " --- "+ issueNodeId )
                    except:
                        helper_methods.logData("Connection rejected")
                        pass
                    # helper_methods.logData("Creating Node between" + json.tostring(user) + "and " json.tostring(issueUrl))

                    count += 1
                    updatedLastPullCount += 1
                    updateConnectLogs(userNodeId, updatedLastPullCount, userNodeId, issueNodeId)
                    helper_methods.logData("UpdatedLastPullCount: " + str(updatedLastPullCount))
                    print("count:" + str(count))

                    if count >= 20:
                        try:
                            saveGraph(g,fileName)
                            count = 0
                        except Exception as e:
                            nx.write_gexf(g, str(fileName))
                            count = 0
                            helper_methods.logData("Graph written as Gexf")
                    # time.sleep(1)
                    time.sleep(0.2)
                except Exception as e:
                    helper_methods.logData(e)
                    updatedLastPullCount += 1
                    time.sleep(5)
                    pass
    return g




def getReposUrlData(reposUrl: str):
    
    reposUrl = reposUrl.replace("'", '"')
    
    reposUrl = json.loads(starredUrl)
    
    return reposUrl['repos_url']



def getParentRepoUrlData(parentRepoUrl):
    parentRepoUrl = parentRepoUrl.replace("'", '"')
    
    parentRepoUrl = json.loads(parentRepoUrl)
    
    return parentRepoUrl['repository_url']

'''
connectUsers(gph)
params: gph -> graph

-> the function tries to connect all users using starred repositories as an edge 
-> we first check the starredUrl in each node
-> we call the starredUrl to get all the repositories starred by the user
-> we store the same in a dictionary along with other users who have the repository starred
-> we make edges across those users


'''
def connectUsers(filename: str):
    # helper_methods.logData("---------Connecting Users---------")
    userToRepo = {}
    temp_dic = {}
    count = 0
    
    while(True):
        try:
            gph = loadGraphGexf(filename)
            helper_methods.logData("graph file found at " + str(filename))
            break
        except Exception as e:
            helper_methods.logData(e)
            # g = nx.Graph()
            helper_methods.logData("unable to load file")
            time.sleep(1)
            helper_methods.logData("reattempting")
    print(gph)
    try:
        with open(fd.connectLogFile, "r") as file:
            prevNodeDetails = json.load(file)
    except Exception as e:
        helper_methods.logData("Unable to pass previous connection file")
        prevNodeDetails = {
            "nodeName" : "NA",
            "nodeNumber" : 0
        }
        helper_methods.logData(e)
        pass
    # with open(fd.connectLogFile, "r") as file:
    #     lastNodeData = json.load(file)
    print(prevNodeDetails)
    repoCount = int(prevNodeDetails['nodeNumber'])
    print(repoCount)
    
    for n in gph.nodes(data=True):
        if(repoCount == 0):    
            if n[1]['bipartite'] == 0:
                starredUrl = n[1]['attr']
                starredUrl = getStarredUrlData(starredUrl)
                starredUrl = starredUrl.strip("{/owner}{/repo}")
                if(starredUrl  == "starred_url"):
                    pass
                else:
                    helper_methods.logData("currently at: " + n[0]) #logging
                    listOfStarredRepos = requests.get(starredUrl, headers = headers)
                    listOfStarredRepos = listOfStarredRepos.json()
                    helper_methods.logData("fetched starred repos" + starredUrl) #logging
                    print("fetched starred repos" + starredUrl)
                    time.sleep(0.1)
                    for repo in listOfStarredRepos:
                        try:
                            tem = repo['name']
                            correctedRepoName = ""
                            for i in tem:
                                if i == '-':
                                    correctedRepoName = correctedRepoName + '_'
                                else:
                                    correctedRepoName = correctedRepoName + i
                        except Exception as e:
                            helper_methods.logData("Error" + str(e))
                            pass
                        # print(ans)
                        if ((correctedRepoName in temp_dic) and (str(n[0]) not in temp_dic[correctedRepoName])):
                            for userName in temp_dic[correctedRepoName]:
                                gph.add_edge(userName,str(n[0]), label=correctedRepoName)
                                count += 1
                            temp_dic[correctedRepoName].append(str(n[0]))
                        else:
                            # print(ans, ans in temp_dic)
                            temp_dic[correctedRepoName] = [str(n[0]),]
                        print(tem)
                    helper_methods.logData("Created Dictionary")
                    saveGraph(gph,fd.finalConnectedGraphFile)
                    helper_methods.logData("A few users connected : - " + str(count) + "  Edges added")
                    prevNodeDetails = {
                        "nodeName" : str(n[0]),
                        "nodeNumber" : int(count)
                    }
                    with open(fd.connectLogFile, "w") as file:
                        file.write(json.dumps(prevNodeDetails))
        else:
            repoCount -= 1
            print("Currently at: " + str(repoCount))      
    
    # # print(temp_dic)
    # for i in temp_dic.keys():
    #     arr = temp_dic[i]
    #     sz = len(arr)
    #     for j in range(0, sz):
    #         for k in range(j + 1, sz):
    #             gph.add_edge(arr[j], arr[k])
    #     try:
    #         saveGraph(gph, "userConnGraph")
    #     except:
    #         try:
    #             nx.write_gml(gph,str(filename))
    #             count = 0
    #         except:
    #             print("unable to write gml")
    #             pass

    #         try:
    #             nx.write_gexf(gph,filename)
    #             count = 0
    #         except:
    #             print("unable to write gexf")
    #             pass
    #     time.sleep(0.2)

    return gph







def connectUsersUsingContrib(filename: str):
    # helper_methods.logData("---------Connecting Users---------")
    userToRepo = {}
    temp_dic = {}
    count = 0
    nodeCount = 0
    
    while(True):
        try:
            gph = loadGraphGexf(filename)
            helper_methods.logData("graph file found at " + str(filename))
            break
        except Exception as e:
            helper_methods.logData(e)
            # g = nx.Graph()
            helper_methods.logData("unable to load file")
            time.sleep(1)
            helper_methods.logData("reattempting")
    print(gph)
    try:
        with open(fd.connectLogFile, "r") as file:
            prevNodeDetails = json.load(file)
    except Exception as e:
        helper_methods.logData("Unable to pass previous connection file")
        prevNodeDetails = {
            "nodeName" : "NA",
            "nodeNumber" : 0
        }
        helper_methods.logData(e)
        pass
    print(prevNodeDetails)
    repoCount = int(prevNodeDetails['nodeNumber'])
    nodeCount = repoCount
    for n in gph.nodes(data=True):
        if(repoCount == 0):
            nodeCount += 1 
            if n[1]['bipartite'] == 0:
                contribUrl = str("https://api.github.com/users/" + str(n[0]) + "/repos")
                if(contribUrl  == "login"):
                    pass
                else:
                    try:
                        helper_methods.logData("currently at: " + n[0]) #logging 
                        try:
                            listOfContribRepos = requests.get(contribUrl, headers = headers)
                            listOfContribRepos = listOfContribRepos.json()
                            helper_methods.logData("fetched starred repos" + contribUrl) #logging
                            time.sleep(0.1)
                        except Exception as e:
                            helper_methods.logData(e)
                            time.sleep(5)
                            helper_methods.logData("=> Some error with requests")
                        for repo in listOfContribRepos:
                            try:
                                tem = repo['name']
                                correctedRepoName = ""
                                for i in tem:
                                    if i == '-':
                                        correctedRepoName = correctedRepoName + '_'
                                    else:
                                        correctedRepoName = correctedRepoName + i
                            except Exception as e:
                                helper_methods.logData("Error" + str(e))
                                pass
                            # print(ans)
                            if ((correctedRepoName in temp_dic) and (str(n[0]) not in temp_dic[correctedRepoName])):
                                for userName in temp_dic[correctedRepoName]:
                                    gph.add_edge(userName,str(n[0]), label=correctedRepoName, type="contribution")
                                    count += 1
                                temp_dic[correctedRepoName].append(str(n[0]))
                            else:
                                # print(ans, ans in temp_dic)
                                temp_dic[correctedRepoName] = [str(n[0]),]
                            print(tem)
                        helper_methods.logData("A few users connected : - " + str(count) + "  Edges added")
                        prevNodeDetails = {
                            "nodeName" : str(n[0]),
                            "nodeNumber" : int(nodeCount)
                        }
                        with open(fd.connectLogFile, "w") as file:
                            file.write(json.dumps(prevNodeDetails))
                    except Exception as e:
                        helper_methods.logData(e)
                        time.sleep(5)
                        continue
        else:
            repoCount -= 1
            print("Currently at: " + str(repoCount))    
        
    saveGraph(gph,"../graphs/v3/contribConnected")  
    

    return gph











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





def connectIssueToIssue(filename):
    helper_methods.logData("Connectig Issues ")
    lastIssue = {}
    try:
        with open(fd.issueLogFile, "r") as file:
            lastIssue = json.load(file)
    except Exception as e:
        helper_methods.logData(e)
        lastIssue = {
            "issueId": "",
            "issueNumber": 0
        }
    
    try:
        with open(fd.issueToLangFile, "r") as file:
            issueToLang = json.load(file)
    except Exception as e:
        helper_methods.logData(e)
        issueToLang = {}
        
    try:
        #  with open(filename, "r") as file:
        gph = loadGraphGexf(filename)  
        helper_methods.logData("Graph Loaded")
        helper_methods.logData(gph)
    except:
        helper_methods.logData("Unable to open graph")
        gph = nx.Graph()
    
    currentIssueCount = int(lastIssue['issueNumber'])
    lastIssueSeen = currentIssueCount
    for n in gph.nodes(data=True):
        if(lastIssueSeen > 0):
            print("Skipping as already attended" + str(n[0]))
            lastIssueSeen -= 1
        else:
            if n[1]['bipartite'] == 1:
                try:
                    parentRepoUrl = n[1]['attr']
                    parentRepoUrl = getParentRepoUrlData(parentRepoUrl)
                    parentRepoUrl = parentRepoUrl.strip("{/owner}{/repo}")
                except Exception as e:
                    helper_methods.logData("Error in reading parent url")
                    helper_methods.logData(e)
                    continue
                # try:
                helper_methods.logData("connecting Issues: " + n[0])
                try:
                    listOfLanguagesUrl = str(parentRepoUrl + "/languages")
                    listOfLanguages = requests.get(listOfLanguagesUrl, headers=headers).json()
                except Exception as e:
                    helper_methods.logData("Some error in fetching files")
                    time.sleep(10)
                    continue
                    
                maxConn = 3
                for item in listOfLanguages:
                    lang = item[0]
                    if lang != None and lang in issueToLang:
                        for issueNode in issueToLang[lang]:
                            gph.add_edge(issueNode,str(n[0]), label=str(item))
                            maxConn -= 1
                            if (maxConn <= 0):
                                break
                        issueToLang[lang].append(str(n[0]))
                    else:
                        issueToLang[lang] = [str(n[0]),]
                filename = str(filename.split(".gexf")[0])
                saveGraph(gph, filename)
            currentIssueCount += 1
            lastIssue = {
                "issueNumber" : int(currentIssueCount),
                "issueId" : str(n[0])
            }
            
            
            try:
                with open(fd.issueLogFile, "w") as file:
                    file.write(json.dumps(issueToLang))
            except Exception as e:
                helper_methods.logData(e)
                pass
            
            try:
                with open(fd.issueToLangFile, "w") as file:
                    file.write(json.dumps(issueToLang))
            except Exception as e:
                helper_methods.logData(e)
                helper_methods.logData("Unable to save logs")
                
                
    return gph



'''
def generateGraph(dataFile, graphFile):

- connect and genrate the full graph based on file name and store the graph


'''


def generateGraph(dataFile, graphFile):
    helper_methods.logData("Generating Graph")
    
    try:
        gph = loadGraphGexf(graphFile)
    except Exception as e:
        helper_methods.logData("No graph file found")
        gph = nx.Graph()
    
    
    # gph = connectUserIssues(graphFile) # generates nodes and edges as well
    # gph = connectIssues(gph)
    # gph = connectUsers(gph)


   
    saveGraph(gph, "fullyConnectedGraph")
    helper_methods.logData("-- Graph Generated --")
    helper_methods.logData("Nodes: " + str(gph.number_of_nodes()))
    helper_methods.logData("Edges: " + str(gph.number_of_edges()))
    helper_methods.logData("-----------------------Compilation Terminating---------------------")

    return gph





    
    reposUrl = reposUrl.replace("'", '"')
    
    reposUrl = json.loads(starredUrl)
    
    return reposUrl['repos_url']

def getLabels(labelUrl):
    labelUrl = labelUrl.replace("'", '"')
    labelUrl = json.loads(labelUrl)
   
    return labelUrl['labels']


def connectIssuesUsingLabels(filename):
    helper_methods.logData("Running Label Connections")
    lastIssue = {}
    try:
        with open(fd.connectLogFile, "r") as file:
            lastIssue = json.load(file)
    except Exception as e:
        helper_methods.logData(e)
        lastIssue = {
            "issueId": "",
            "issueNumber": 0
        }
    
    try:
        with open(fd.dataLogFile, "r") as file:
            issueToLabel = json.load(file)
            
    except Exception as e:
        helper_methods.logData(e)
        commonLabels = ["bug","documentation","duplicate","enhancement","help wanted","invalid","question","wontfix","discussion","epic","needs information"]
        issueToLabel = {}
        for lab in commonLabels:
             issueToLabel[lab] = []
    print(lastIssue)
    currentIssueCount = lastIssue['issueNumber']
    lastIssueCount = currentIssueCount
    
        
    try:
        #  with open(filename, "r") as file:
        gph = loadGraphGexf(filename)  
        helper_methods.logData("Graph Loaded")
        helper_methods.logData(gph)
    except:
        helper_methods.logData("Unable to open graph")
        gph = nx.Graph()
        
        
    for n in gph.nodes(data=True):
        if(lastIssueCount != 0):
            lastIssueCount -= 1
        else:   
            currentIssueCount += 1     
            if(n[1]['bipartite'] == 1):
                try:
                    labelsUrl = n[1]['attr']
                    listOfLabels = getLabels(labelsUrl)
                except Exception as e:
                    helper_methods.logData("Error in reading parent url")
                    helper_methods.logData(e)
                    continue
                # try:
                helper_methods.logData("connecting Issues: " + n[0])
                # try:
                    
                #     listOfLabels = requests.get(labelsUrl, headers=headers).json()
                # except Exception as e:
                #     helper_methods.logData("Some error in fetching files")
                #     time.sleep(10)
                #     continue
                
                if(listOfLabels == [] or listOfLabels == None):
                    helper_methods.logData("No labels found for issue")
                    continue
                    
                for item in listOfLabels:
                    labelName = item[0]
                    
                    time.sleep(100)
                    if labelName != None and labelName in issueToLabel:
                        for issueNode in issueToLabel[labelName]:
                            gph.add_edge(issueNode,str(n[0]), label=str(item))
                        issueToLabel[labelName].append(str(n[0]))
                    else:
                        issueToLabel[labelName] = [str(n[0]),]
                # filename = str(filename.split(".gexf")[0])
                # saveGraph(gph, filename)
            currentIssueCount += 1
            lastIssue = {
                "issueNumber" : int(currentIssueCount),
                "issueId" : str(n[0])
            }
            
            
            try:
                with open(fd.connectLogFile, "w") as file:
                    file.write(json.dumps(lastIssue))
            except Exception as e:
                helper_methods.logData(e)
                pass
            
            
            
            try:
                with open(fd.dataLogFile, "w") as file:
                    file.write(json.dumps(issueToLabel))
            except Exception as e:
                helper_methods.logData(e)
                pass
                
                
    return gph
                
                
    
        
        


# connectUsers(fd.userToIssueConnFileMinor)
# connectIssueToIssue(fd.finalConnectedGraphFile)
# connectUsersUsingContrib("../graphs/final/finalConnectedGraph.gexf")
# generateGraph(fd.pullsFile,"../graphs/finalGraph.gexf")
connectIssuesUsingLabels("../graphs/v3/contribConnected.gexf")

# gph = connectUsers(fd.userToIssueConnFileMinor)

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
'''