
import json
from pprint import pprint
import requests

import s1_fast_user
import s2_fast_repos
import utils.helper_methods as helper_methods

# Repo struct
def getRepoStruct(org):
    users = s1_fast_user.getUsers(org)
    repos = s2_fast_repos.getRepos(org)

    helper_methods.whereAmI()
    repoStruct = {}
    for repo in repos:
        tempStruct={}
        tempStruct["users"] = filterMembers(getContriForRepo(org, repo), users)
        tempStruct["topics"] = getRepoTopics(org,repo)
        tempStruct["languages"] = getRepoLanguages(org, repo)
        repoStruct[repo]=tempStruct
    json.dump(repoStruct, open('data/output/repoStruct/'+org+'.json', 'w'))
    print("repoStruct built")
    return repoStruct

def getRepoTopics(org, repo):
    headers = helper_methods.seekHeaders()
    topics = []
    repoURL = 'https://api.github.com/repos/'+org+'/'+repo
    repoURLRes = requests.get(repoURL, headers=headers).json()
    topics = repoURLRes["topics"]
    return topics

def getRepoLanguages(org, repo):
    headers = helper_methods.seekHeaders()
    repoURL = 'https://api.github.com/repos/'+org+'/'+repo+'/languages'
    repoURLRes = requests.get(repoURL, headers=headers).json()
    languages = []
    for key in iter(repoURLRes):
        languages.append(key)
    return languages

def getContriForRepo(org, repo):
    helper_methods.whereAmI()
    headers = helper_methods.seekHeaders()
    contributorUrl = 'https://api.github.com/repos/'+org+'/'+repo+'/contributors'
    contributors = []
    pageNo = 1
    while(True):
        contributorResponse = requests.get(
            contributorUrl+'?page='+str(pageNo), headers=headers).json()
        if(len(contributorResponse) == 0):
            break
        pageNo = pageNo+1
        for contributor in contributorResponse:
            contributors.append(contributor["login"])
    return contributors

def filterMembers(contributors, userList):
    helper_methods.whereAmI()
    memberContributors = []
    for contributor in contributors:
        if contributor in userList:
            memberContributors.append(contributor)
    return memberContributors

def getRepoCreationDate():
    pass
    
# User struct
def getUserStruct(org):
    helper_methods.whereAmI()
    userStruct = {}
    repoStruct = json.load(open('data/output/repoStruct/'+org+'.json', 'r'))
    users = s1_fast_user.getUsers(org)
    for user in users:
        tempStruct={}
        repoList,topicList,languageList = [],[],[]
        for repo in repoStruct:
            if user in repoStruct[repo]["users"]:
                repoList.append(repo)
                topicList.extend(repoStruct[repo]["topics"])
                languageList.extend(repoStruct[repo]["languages"])
        tempStruct["repos"] = repoList
        tempStruct["topics"] = list(set(topicList))
        tempStruct["languages"] = list(set(languageList))
        userStruct[user]=tempStruct
    json.dump(userStruct, open('data/output/userStruct/'+org+'.json', 'w'))
    print("userStruct built")
    return userStruct
