'''
    Given a repoStruct - what are the repo repo edge list
    Input: repoStruct, Returns: repo repo edge list

'''
import json
import os
from itertools import permutations

import s3_buildStructs
import utils.helper_methods as helper_methods


def getRepoRepoEL(org):
    helper_methods.whereAmI()
    repoRepoEL = []
    if not os.path.exists('data/output/repoStruct/'+org+'.json'):
        repoStruct = s3_buildStructs.getRepoStruct(org)
    repoStruct = json.load(open('data/output/repoStruct/'+org+'.json', 'r'))
    # add user user edge lists
    repos=list(repoStruct.keys())
    for i in range(len(repos)):
        for j in range(i+1, len(repos)):
            repo1=repos[i]
            repo2=repos[j]
            common_languages = set(repoStruct[repo1]["languages"]).intersection(
                set(repoStruct[repo2]["languages"]))

            if common_languages:
                repoRepoEL.append((repo1,repo2))
    # remove (b,a) if (a,b) exists
    # for tup in repoRepoEL:
    #     if (tup[1], tup[0]) in repoRepoEL:
    #         repoRepoEL.remove((tup[1], tup[0]))
    edgeWeights=getEdgeWeight(repoRepoEL,repoStruct)
    return repoRepoEL,edgeWeights

# TODO Check edgeWeights
def getEdgeWeight(repoRepoEL,repoStruct):
    edgeWeights=[]
    for repoPair in repoRepoEL:
        numOfOverlapping=len(list(set(repoStruct[repoPair[0]]['languages']).intersection(set(repoStruct[repoPair[0]]['languages'])))) 
        edgeWeights.append(numOfOverlapping)
    return edgeWeights