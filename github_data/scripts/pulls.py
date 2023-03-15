import json
import time
import requests
import utils.helper_methods as helper_methods
import queue
import users as users
import sys
sys.path.append('../')

def getPulls(repo):
    helper_methods.logData("getPulls called")
    pulls = []
    linked_issues = []
    linked_users = []
    # headers = helper_methods.seekHeaders()
    headers = {"Authorization": "Bearer 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"}
    pullUrl = str('https://api.github.com/repos/' + repo + '/pulls?state=closed')
    helper_methods.logData(f"pulls from current repo: {pullUrl}")
    pageNo = 1
    pull_requests = []
    # while(True):
    pullsResponse = requests.get(pullUrl, headers=headers)
    pullsResponse=pullsResponse.json()
    print(pullsResponse)
    # if(len(pullsResponse) == 0):
    #     break
    # pageNo = pageNo+1
    for pr in pullsResponse:
        pull_requests.append(pr)
        linkedIssueData = requests.get(str(pr['issue_url']), headers=headers) # one issue 
        linkedIssueData = linkedIssueData.json()
        linkedUserData = pr['user'] # one user 
        linked_issues.append(linkedIssueData)
        linked_users.append(linkedUserData)


    json_object = json.dumps(pullsResponse, indent=4)
    with open("../data/raw/pulls.json", "a") as outfile:
        outfile.write(json_object)
    user_json_object = json.dumps(linked_users, indent=4)
    with open("../data/raw/users.json", "a") as outfile:
        outfile.write(user_json_object)
    issue_json_object = json.dumps(linked_issues, indent=4)
    with open("../data/raw/pull_issues.json", "a") as outfile:
        outfile.write(issue_json_object)
    
    time.sleep(0.1)

    return pulls

# print(getUsers('yahoo'))



def fetchPullData():
    repoList = helper_methods.getRepoList()

    repoCount = 0
    for repo in repoList:
        getPulls(repo)
        repoCount += 1
        helper_methods.logCurrentRepo(repo, repoCount)
        helper_methods.logData(f"fetchIssueData: Fetching Issues -> {repo}")
        # print(repo)

        time.sleep(0.5)

# fetchPullData()