'''
    1) Given an org - give the list of members
    These are the user nodes in the graph

    call: getUsers(org), returns list of users
'''

import requests
import utils.helper_methods as helper_methods
import sys
sys.path.append('../')

headers = {"Authorization": "Bearer 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"}

orgList = []



    



def getUsers(org):
    helper_methods.whereAmI()
    members = []
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



def appendUsersToUserList(currUser,appendQueue,level, levelLimit):
    if(level >= levelLimit):
        print("Level limit reached")
        return appendQueue
    else:
        userFollowerUrl = currUser # write the url link 
        followerList = requests.get(userFollowerUrl, headers=headers)
        for x in followerList:
            appendQueue.put(x)
        level += 1
        return appendQueue

# print(getUsers('yahoo'))



def fetchUserData():
    userList = helper_methods.getUserList()
    userCount = 0
    userFetchLevel = 5
    user_queue = queue.Queue()
    for val in userList:
        currentlevel = 0
        while user_queue.empty() == False:
            user = user_queue.get()
            getUsers(user)
            appendUsersToUserList(user,user_queue, currentlevel, userFetchLevel)
            userCount += 1
            
        user_queue.put(val)