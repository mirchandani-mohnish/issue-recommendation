
import pandas as pd


def whereAmI():
    print()



def seekHeaders():
    print("Seeking Headers")







def getToken():
    print("Getting Token")


def getRepoList():
    rawRepoList = pd.read_csv(r'data/repos.csv')
    filteredRepoList = []
    for row in rawRepoList['repo_url']:
        repoName = row.split("https://github.com/")
        filteredRepoList.append(repoName[1])
    
    return filteredRepoList

def logCurrentRepo(repo, repoCount):
    with open("data/logs.json", "a") as outfile:
        outfile.write(str(repoCount))
        outfile.write("/t")
        outfile.write(repo)
        outfile.write("/n")
    print(str(repoCount) + " " + repo)
    
    



getRepoList()