import issues as issues
import time
import utils.helper_methods as helper_methods




def fetchIssueData():
    repoList = helper_methods.getRepoList()
    repoCount = 0
    for repo in repoList:
        issues.getIssues(repo)
        repoCount += 1
        helper_methods.logCurrentRepo(repo, repoCount)
        # print(repo)

        time.sleep(0.5)



fetchIssueData()