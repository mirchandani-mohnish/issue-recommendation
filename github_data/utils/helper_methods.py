
import pandas as pd
import sys
import requests
sys.path.append('../')

def whereAmI():
    print()



def seekHeaders():
    print("Seeking Headers")







def getToken():
    print("Getting Token")


def getRepoList():
    rawRepoList = pd.read_csv(r'../data/input/repos.csv')
    filteredRepoList = []
    for row in rawRepoList['repo_url']:
        repoName = row.split("https://github.com/")
        filteredRepoList.append(repoName[1])
    
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
    repoUrl = "https://api.github.com/search/users?q=type:org"
    orgData = requests.get(repoUrl, headers=headers)
    for org in orgData['items']:
        orgDataFiltered = org['login']
        print(org['login'])
    # rawRepoList = pd.read_csv(r'../data/input/repos.csv')
    # logData("generating org list from repos.csv file")
    # filteredRepoList = []
    # for row in rawRepoList['repo_url']:
    #     repoName = row.split("https://github.com/")
    #     repoName = repoName[1].split("/")
    #     filteredRepoList.append(repoName[0])
    #     print(repoName[1])
    # return filteredRepoList


    
    # return filteredRepoList

def logCurrentRepo(repo, repoCount):
    with open("../data/logs/repologs.json", "a") as outfile:
        outfile.write(str(repoCount))
        outfile.write("/t")
        outfile.write(repo)
        outfile.write("/n")
    print(str(repoCount) + " " + repo)
    
    
def logData(logVal):
    with open("../data/logs/logs.json", "a") as outfile:
        outfile.write(str(logVal))
        outfile.write("\n")
    print(logVal)

getOrgList()