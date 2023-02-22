import requests
from pprint import pprint
import json
from utils.helper_methods import shouldIReset
import os

def get_repo_details_from_file(org,repo):
    with open("data/output/enhanced-repo/"+org+"_new.json", "r") as file:
        enhancedOrg=json.load(file)
    return enhancedOrg[repo]

def get_repo_details(org,repo, access_token):
    repo_url=org+"/"+repo
    # if not os.path.isfile("data/output/enhanced-repo/"+org+".json"):
    repo_url = "https://api.github.com/repos/"+repo_url
    repo_info = get_repo_info(repo_url, access_token)
    creation_date = get_creation_date(repo_info)
    stargazers = get_stargazers_usernames(repo_url, access_token)
    watchers = get_watchers_usernames(repo_url, access_token)
    forks_count = get_forks_count(repo_info)
    commit_count = get_commit_count(repo_url, access_token)
    topics, languages = get_topics_and_languages(repo_url, access_token)
    return {
        "Creation Date": creation_date,
        "Stargazers": stargazers,
        "Watchers": watchers,
        "Forks Count": forks_count,
        "Commit Count": commit_count,
        "Topics": topics,
        "Languages": languages
    }
    # else:
    #     with open("data/output/enhanced-repo/"+org+".json","r") as file:
    #         enhancedOrg=json.load(file)
    #     return enhancedOrg[repo]

def get_repo_info(repo_url, access_token):
    headers = {
        "Authorization": "Token " + access_token
    }
    shouldIReset()
    response = requests.get(repo_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_creation_date(repo_info):
    if repo_info:
        return repo_info['created_at']
    return None

def get_stargazers_usernames(repo_url, access_token):
    stargazers_url = repo_url + "/stargazers"
    stargazers=doUntilNone(stargazers_url,access_token)
    return [stargazer['login'] for stargazer in stargazers]
    
def get_watchers_usernames(repo_url, access_token):
    watchers_url = repo_url + "/subscribers"
    watchers=doUntilNone(watchers_url,access_token)
    return [watcher['login'] for watcher in watchers]

def get_forks_count(repo_info):
    if repo_info:
        return repo_info['forks_count']
    return None

def get_commit_count(repo_url, access_token):
    commits_url = repo_url + "/commits"
    commits=doUntilNone(commits_url,access_token)
    # commitTimeStamps=[commit['commit']['author']['date'] for commit in commits]
    return len(commits)


def get_topics_and_languages(repo_url, access_token):
    headers = {
        "Authorization": "Token " + access_token,
        "Accept": "application/vnd.github+json"
    }
    topics_url = repo_url + "/topics"
    shouldIReset()
    topics=requests.get(topics_url,headers=headers).json()['names']
    languages_url=repo_url+"/languages"
    shouldIReset()
    languages=list(requests.get(languages_url,headers=headers).json().keys())
    return(topics,languages)

def doUntilNone(url,access_token):
    headers = {
        "Authorization": "Token " + access_token,
        "Accept": "application/vnd.github+json"
    }
    dataList=[]
    pageNo=1
    while(True):
        shouldIReset()
        response = requests.get(url+'?page='+str(pageNo), headers=headers)
        if response.status_code == 200:
            if (len(response.json())==0):
                break
            dataList.extend(response.json())
            pageNo+=1
        else:
            pass
    return dataList
# org="10up"
# # org="10gen"
# orgData={}
# with open("data/output/enhanced-repo/"+org+".json", "w") as file:
#     json.dump(orgData, file)
# with open("data/output/repoStruct/"+org+".json","r") as file:
#     data=json.load(file)
# repoList=list(data.keys())
# # # repoList=["mgo"]
# for repo in repoList:
#     repo_url = org+"/"+repo
#     print(repo_url)
#     orgData[repo]=get_repo_details(org=org,repo=repo,access_token=access_token)
#     with open("data/output/enhanced-repo/"+org+".json", "w") as file:
#         json.dump(orgData, file)
