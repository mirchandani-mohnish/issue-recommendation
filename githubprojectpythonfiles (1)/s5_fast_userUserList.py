'''
    Given a userStruct - what are the user user edge list
    Input: userStruct, Returns: user user edge list

'''
import json
import os
from itertools import permutations

import s3_buildStructs
import utils.helper_methods as helper_methods

def getUserUserEL(org):
    helper_methods.whereAmI()
    userUserEL=[]
    if not os.path.exists('data/output/repoStruct/'+org+'.json'):
        repoStruct = s3_buildStructs.getRepoStruct(org)
    repoStruct = json.load(open('data/output/repoStruct/'+org+'.json', 'r'))
    # add user user edge lists
    for repo in repoStruct:
        permutationList=tuple(permutations(repoStruct[repo]['users'],2))
        userUserEL.extend(permutationList)
    # remove (b,a) if (a,b) exists
    for tup in userUserEL:
        if (tup[1], tup[0]) in userUserEL:
            userUserEL.remove((tup[1], tup[0]))
    return userUserEL