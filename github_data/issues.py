'''
    1) Given an org - give the list of members
    These are the user nodes in the graph

    call: getUsers(org), returns list of users
'''

import requests
import utils.helper_methods as helper_methods

def getIssues(org):
    helper_methods.whereAmI()
    issues = []
    headers = helper_methods.seekHeaders()
    orgUrl = 'https://api.github.com/orgs/'+org+'/issues'
    pageNo = 1
    while(True):
        issueResponse = requests.get(orgUrl+'?page='+str(pageNo), headers=headers)
        issueResponse=issueResponse.json()
        if(len(issueResponse) == 0):
            break
        pageNo = pageNo+1
        for issue in issueResponse:
            issues.append(issue)
    return issues

# print(getUsers('yahoo'))