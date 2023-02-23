import issues as issues
import time
import utils.helper_methods as helper_methods


def fetchIssueData():
    repoList = helper_methods.getRepoList()
    for repo in repoList:
        issues.getIssues(repo)
        print(repo)

        time.sleep(0.5)



fetchIssueData()