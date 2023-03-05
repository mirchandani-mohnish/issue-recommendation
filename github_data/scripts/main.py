import sys
sys.path.append('../')

import time
import utils.helper_methods as helper_methods
import users as users
import issues as issues
import datetime
import json
import threading
import pulls as pulls

helper_methods.logData("-----------New Compile---------")
dt = datetime.date.today()
helper_methods.logData(str(dt))
helper_methods.logData("Main Function File Called")


def logUsers(userData):
    helper_methods.logData("Users being fetched")
    json_object = json.dumps(userData, indent=4)
    with open("../data/raw/users.json", "a") as outfile:
        outfile.write(json_object)
    return

def fetchUsersViaOrgs():
    orgList = []

    with open("../data/raw/orgs.json", "r") as infile:
        for line in infile:
            line.strip()
            orgList.append(str(line).strip())
        

    helper_methods.logData("Done Reading Org List")

    for org in orgList:
        print(org)
        userData = users.getUsers(org)
        print(userData)
        # logUsers(userData)
        time.sleep(1)


def fetchIssueUsersPulls():
    pulls.fetchPullData()


fetchIssueUsersPulls()