import requests
import utils.helper_methods as helper_methods
import sys
sys.path.append('../')

headers = {"Authorization": "Bearer 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"}


'''
getUsers()

The get users call gets the users of a single organization
-> users fetched are stored in a json file
-> we handle pagination provided by github pages also

'''
def getUsers(org):
    helper_methods.logData(f"User Fetch Called: {org}")
    members = []
    orgUrl = 'https://api.github.com/orgs/'+org+'/members'
    pageNo = 1
    while(True):
        memberResponse = requests.get(orgUrl+'?page='+str(pageNo), headers=headers)
        print(orgUrl+'?page='+str(pageNo))
        memberResponse=memberResponse.json()
        if(len(memberResponse) == 0 or memberResponse['message'] == "Not Found"):
            print(memberResponse)
            break
        pageNo = pageNo+1
        for member in memberResponse:
            members.append(member)
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


'''
fetchUserData
-> fetch user data is a function which provides for fetching user data
-> it provides a sort of breadth first approach. 

'''

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

