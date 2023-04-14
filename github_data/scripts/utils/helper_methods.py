
import pandas as pd
import sys
import requests
import time
sys.path.append('../')





def seekHeaders():
    print("Seeking Headers")



def replace_brackets_with_comma(file_path):
    with open(file_path, 'r+') as file:
        content = file.read()
        updated_content = content.replace(",,", ",")
        file.seek(0)
        file.write(updated_content)
        file.truncate()
    print("done")


def getToken():
    print("Getting Token")


def appendToFile(filePath, data):
    print()

def getRepoList(lastRepoCount, lastRepoName):
    rawRepoList = pd.read_csv(r'../data/input/repos.csv')
    filteredRepoList = []
    RepoList = rawRepoList.iloc[lastRepoCount: , :]
    for row in RepoList['repo_url']:
        repoName = row.split("https://github.com/")
        filteredRepoList.append(repoName[1])
        # print(repoName[1])
        
    
    return filteredRepoList

# def getOrgList():
#     rawRepoList = pd.read_csv(r'../data/input/repos.csv')
#     logData("generating org list from repos.csv file")
#     filteredRepoList = []
#     for row in rawRepoList['repo_url']:
#         repoName = row.split("https://github.com/")
#         repoName = repoName[1].split("/")
#         filteredRepoList.append(repoName[0])
#         print(repoName[1])
#     return filteredRepoList

headers = {"Authorization": "Bearer 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"}

def getOrgList():
    repoUrl = 'https://api.github.com/search/users?q=type:org' 
    pageNo = 1
    orgDataFilteredList = []
    logData("getting organization details from github")
    while(True):
        orgData = requests.get(repoUrl + '?page='+str(pageNo), headers=headers)
        orgData = orgData.json()
        logData(repoUrl + '?page='+str(pageNo))
        if(len(orgData) == 0):
            break
        pageNo += 1
        logData("page no: " + str(pageNo))
        for org in orgData['items']:
            orgDataFiltered = org['login']
            orgDataFilteredList.append(orgDataFiltered)
            with open("../data/raw/orgs.json", "a") as outfile:
                outfile.write(str(org['login']))
                outfile.write("\n") 
            logData("currentOrg: " + str(org['login']))
            time.sleep(0.5)
        
        
    return orgDataFilteredList 
    # rawRepoList = pd.read_csv(r'../data/input/repos.csv')
    # logData("generating org list from repos.csv file")
    # filteredRepoList = []
    # for row in rawRepoList['repo_url']:
    #     repoName = row.split("https://github.com/")
    #     repoName = repoName[1].split("/")
    #     filteredRepoList.append(repoName[0])
    #     print(repoName[1])
    # return filteredRepoList


    # 
    # return filteredRepoList

def logCurrentRepo(repo, repoCount):
    with open("../data/logs/repologs.json", "a") as outfile:
        outfile.write(str(repoCount))
        outfile.write("/t")
        outfile.write(repo)
        outfile.write("/n")
    print(str(repoCount) + " " + repo)
    
    
def logData(logVal):
    with open("../../data/logs/logs.json", "a") as outfile:
        outfile.write(str(logVal))
        outfile.write("\n")
    print(logVal)


