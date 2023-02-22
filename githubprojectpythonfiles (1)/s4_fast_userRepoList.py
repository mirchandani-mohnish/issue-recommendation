
import utils.helper_methods as helper_methods
import json
import os

import s3_buildStructs

def getUserRepoEL(org):
    if not os.path.exists('data/output/repoStruct/'+org+'.json'):
        repoStruct = s3_buildStructs.getRepoStruct(org)
    if not os.path.exists('data/output/userStruct/'+org+'.json'):
        userStruct=s3_buildStructs.getUserStruct(org)
    repoStruct = json.load(open('data/output/repoStruct/'+org+'.json', 'r'))
    userStruct = json.load(open('data/output/userStruct/'+org+'.json', 'r'))
    users=list(userStruct.keys())
    repos=list(repoStruct.keys())
    return userRepoEdgeList(repoStruct),users,repos,userStruct,repoStruct

def userRepoEdgeList(repoStruct):
    helper_methods.whereAmI()
    userRepoEL = []
    for repo in repoStruct:
        for user in repoStruct[repo]["users"]:
            edge = (user, repo)
            userRepoEL.append(edge)
    return userRepoEL