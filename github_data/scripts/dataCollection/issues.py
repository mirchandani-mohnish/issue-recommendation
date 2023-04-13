'''
    1) Given an org - give the list of members
    These are the user nodes in the graph

    call: getUsers(org), returns list of users
'''
import json
import time
import requests
import utils.helper_methods as helper_methods
import queue
import github_data.scripts.dataCollection.users as users
import sys
sys.path.append('../')



'''
getIssues function
-> used to get issues based on call from repository
-> pass repository as a parameter and will continuously place call to the link
-> takes care of pagination by running a loop till all issues fetched


'''
def getIssues(repo):
    helper_methods.logData("getIssues called")
    issues = []
    # headers = helper_methods.seekHeaders()
    headers = {"Authorization": "Bearer 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"}
    orgUrl = 'https://api.github.com/repos/'+repo+'/issues'
    helper_methods.logData(f"Issues from current repo: {orgUrl}")
    pageNo = 1
    while(True):
        issueResponse = requests.get(orgUrl+'?page='+str(pageNo), headers=headers)
        issueResponse=issueResponse.json()
        if(len(issueResponse) == 0):
            break
        pageNo = pageNo+1
        for issue in issueResponse:
            issues.append(issue)
        helper_methods.logData(f"getIssues: IssuePageNumber: {pageNo}")
        json_object = json.dumps(issueResponse, indent=4)
        with open("data/issues.json", "a") as outfile:
            outfile.write(json_object)
 
        # Writing to sample.json
        # with open("./data/issues.json", "r+") as outfile:
        #     json_data = json.loads(outfile.read())
        #     json_data.append(issues)
        #     json.dump(json_data, outfile)
        
        time.sleep(0.1)

    return issues

# print(getUsers('yahoo'))




def getIssueStruct(org):
    helper_methods.whereAmI()
    issueStruct = {}
    # repoStruct = json.load(open('data/output/repoStruct/'+org+'.json', 'r'))
    issueStruct = getIssues(org)
    # for issue in issues:
    #     tempStruct={}
    #     # repoList,topicList,languageList = [],[],[]
    #     # for repo in repoStruct:
    #     #     if user in repoStruct[repo]["users"]:
    #     #         repoList.append(repo)
    #     #         topicList.extend(repoStruct[repo]["topics"])
    #     #         languageList.extend(repoStruct[repo]["languages"])
    #     # tempStruct["repos"] = repoList
    #     # tempStruct["topics"] = list(set(topicList))
    #     # tempStruct["languages"] = list(set(languageList))
    #     # userStruct[user]=tempStruct
    json.dump(issueStruct, open('data/issueStruct/'+org+'.json', 'w'))
    json.dump(issueStruct, open('data/issues.json', 'w'))
    print("userStruct built")
    return issueStruct



'''
fetchIssueData()
-> function used to fetch all issue data
-> uses getIssues as a utility
-> takes the repolist provided in getRepoList function 
-> repos.csv consists of the popular repositories of 2022
'''


def fetchIssueData():
    repoList = helper_methods.getRepoList()

    repoCount = 0
    for repo in repoList:
        getIssues(repo)
        repoCount += 1
        helper_methods.logCurrentRepo(repo, repoCount)
        helper_methods.logData(f"fetchIssueData: Fetching Issues -> {repo}")
        # print(repo)

        time.sleep(0.5)


