'''
    1) Given an org - give the list of repos
    These are the repo nodes in the org

    call: getRepos(org), returns list of repos
'''

import requests
import utils.helper_methods as helper_methods

def getRepos(org):
    helper_methods.whereAmI()
    repos = []
    headers = helper_methods.seekHeaders()
    pageNo=1
    baseRepoUrl = 'https://api.github.com/orgs/'
    while(True):
        response = requests.get(baseRepoUrl+org+'/repos?page='+str(pageNo),headers=headers)
        response = response.json()
        if(len(response) == 0):
            break
        pageNo = pageNo+1
        for repo in response:
            repos.append(repo['name'])
    return repos


# print(getRepos('yahoo'))
