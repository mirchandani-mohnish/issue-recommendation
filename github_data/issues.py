'''
    1) Given an org - give the list of members
    These are the user nodes in the graph

    call: getUsers(org), returns list of users
'''

import requests
import utils.helper_methods as helper_methods

def getUsers(org):
    helper_methods.whereAmI()
    members = []
    headers = helper_methods.seekHeaders()
    orgUrl = 'https://api.github.com/orgs/'+org+'/members'
    pageNo = 1
    while(True):
        memberResponse = requests.get(orgUrl+'?page='+str(pageNo), headers=headers)
        memberResponse=memberResponse.json()
        if(len(memberResponse) == 0):
            break
        pageNo = pageNo+1
        for member in memberResponse:
            members.append(member['login'])
    return members

# print(getUsers('yahoo'))