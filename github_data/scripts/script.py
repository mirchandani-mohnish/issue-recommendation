import requests
import json
import time
import sys
sys.path.append('../')
# Define the repository for which you want to extract issues data
repo = "lapce/lapce"

# Define the API endpoint for the issues data
url = "https://api.github.com/repos/" + repo + "/issues"

# Define the interval in seconds between each iteration
interval = 30

while True:
    # Make a GET request to the API endpoint
    response = requests.get(url)

    # Check if the API request was successful
    if response.status_code == 200:
        # Extract the JSON data from the response
        data = json.loads(response.text)
        json_object = json.dumps(data, indent=4)
 
# Writing to sample.json
        with open("sample.json", "w") as outfile:
            outfile.write(json_object)
        # Loop through the issues and print the title and state of each issue
        for issue in data:
            print("Title: ", issue["title"])
            print("State: ", issue["state"])
            print("-----------------------------")
    else:
        # If the API request was not successful, print an error message
        print("Failed to retrieve issues data from the API.")

    # Wait for the specified interval before the next iteration
    time.sleep(interval)




