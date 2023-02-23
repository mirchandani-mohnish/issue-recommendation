'''
    1) Given an org - give the list of members
    These are the user nodes in the graph

    call: getUsers(org), returns list of users
'''
import json
import time
import requests
import utils.helper_methods as helper_methods

def getIssues(repo):
    helper_methods.whereAmI()
    issues = []
    # headers = helper_methods.seekHeaders()
    headers = {"Authorization": "Bearer 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"}
    orgUrl = 'https://api.github.com/repos/'+repo+'/issues'
    pageNo = 1
    while(True):
        issueResponse = requests.get(orgUrl+'?page='+str(pageNo), headers=headers)
        issueResponse=issueResponse.json()
        if(len(issueResponse) == 0):
            break
        pageNo = pageNo+1
        for issue in issueResponse:
            issues.append(issue)
        print(issueResponse)
        json_object = json.dumps(issueResponse, indent=4)
 
        # Writing to sample.json
        with open("./data/issues.json", "w") as outfile:
            outfile.append(json_object)
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




# getIssueStruct('lapce/lapce')