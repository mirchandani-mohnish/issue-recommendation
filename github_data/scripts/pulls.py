import json
import time
import requests
import utils.helper_methods as helper_methods
import queue
import users as users
import sys
import fileDefinitions as fd
import os

sys.path.append('../')




'''
Pull requests in github become the connection bridge between users and issues
-> pull requests also have issueUrl and user data.
-> we use both to form graphs

'''




def getPulls(repo):
    helper_methods.logData("getPulls called")
    pulls = []
    linked_issues = []
    linked_users = []
    accessToken = ""
    # headers = helper_methods.seekHeaders()
    with open(fd.helperFile, "r") as file:
        accessToken = json.load(file)['token']
    headers = {"Authorization": "Bearer " + accessToken }


    pullUrl = str('https://api.github.com/repos/' + repo + '/pulls?state=closed')
    helper_methods.logData(f"pulls from current repo: {pullUrl}")
    pageNo = 1
    pull_requests = []
    # while(True):
    try: 
        pullsResponse = requests.get(pullUrl, headers=headers)
        pullsResponse=pullsResponse.json()
    except Exception as e:
        helper_methods.logData(e)
        return pulls

    # print(pullsResponse)
    # if(len(pullsResponse) == 0):
    #     break
    # pageNo = pageNo+1
    for pr in pullsResponse:
        try: 
            pull_requests.append(pr)
            # linkedIssueData = requests.get(str(pr['issue_url']), headers=headers) # one issue 
            # linkedIssueData = linkedIssueData.json()
            linkedUserData = pr['user'] # one user 
            # linked_issues.append(linkedIssueData)
            linked_users.append(linkedUserData)
        except Exception as e:
            helper_methods.logData(e)
            pass


    json_object = json.dumps(pullsResponse, indent=4)
    with open(fd.pullsFile, "a") as outfile:
        outfile.write(json_object)
    user_json_object = json.dumps(linked_users, indent=4)
    with open(fd.usersFile, "a") as outfile:
        outfile.write(user_json_object)
    # issue_json_object = json.dumps(linked_issues, indent=4)
    # with open(fd.issuesFile, "a") as outfile:
    #     outfile.write(issue_json_object)
    time.sleep(0.1)

    return pulls

# print(getUsers('yahoo'))



def fetchPullData():
    lastpull = {}
    with open(fd.dataLogFile, "r") as dataFile:
        lastpull = json.load(dataFile)

    lastRepoCount = lastpull["repoCount"]
    print(lastRepoCount)
    lastRepoName = lastpull["lastRepo"]
    
    repoList = helper_methods.getRepoList(lastRepoCount, lastRepoName)
    
    
    for repo in repoList:
        getPulls(repo)
        lastRepoCount += 1
        helper_methods.logCurrentRepo(repo, lastRepoCount)
        helper_methods.logData(f"fetchIssueData: Fetching Issues -> {repo}")
        dataLog = {
            'lastRepo' : repo,
            'repoCount' : lastRepoCount
        }
        with open(fd.dataLogFile, "w") as outfile:
            jsonDataLog = json.dumps(dataLog, indent=4)
            outfile.write(jsonDataLog)
        # print(repo)
        time.sleep(0.2)

fetchPullData()