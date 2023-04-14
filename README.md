# Codetriaging: The SNAzzy Way

A project by:

- AU2040004 - Priya Jani
- AU2040028 - Yansi Memdani
- AU2040110 - Mohnish Mirchandani
- AU2040241 - Priyanshu Pathak

## How to run the code

### Requirements

- Python >=v3.4
- Pandas == 1.5.3
- networkx == 3.0
- matplotlib == 3.6.3
- numpy == 1.23.5
- python pickle

Additionally, an extension in VScode for running ipynb files is recommended.

### Running the graph

Assuming you have a pre-generated graph ready. You can run the file labeled `script.py`. The same consists of helper code to help you out along the way.

You may run the files respectively in order to generate predictions. Additionally each algorithmic implementation has accuracy measured and mapped in the particular algorithm files.

### File Definitions

The Following algorithms were implemented in the project:

- Adamic Adar
- Jaccard Coefficient
- Preferential Attachment
- Resource Allocation
- Weighted Projection Algorithm
- GLHub ( Self-Developed Algorithm )

Each of the files are isolated ipynb files which can be run and tested.

## Methodology

### Data Collection

A considerable amount of time went in data collection specifically because of first-hand data collection for the project. The same was done using the currently presented github api. Additionally, Github API had a limit of 1000 queries per hour for personal users. The following data was collected for the project

- A set of Issues
- A set of Users
- A set of Pull Requests
- The Languages of each issue
- The Contributions of Each User

## Graphs

The code has majorly been tested on two graphs of similar configurations but varying scales. The configuration of our graphs is as follows:

**Nodes (types)**:

- User
- Issue

**Edges**:

- User --- User -> Commonly Contributed Repositories
- User --- User -> Commonly Starred Repositories
- User --- Issue -> Contribution
- Issue --- Issue -> Common Languages of Parent Repository

### Graph 1

- A cumulative of 11000 Nodes and 291375 edges
- Around 3000 users and 8000 issues

You may find the graphs here: [click here](https://drive.google.com/drive/folders/1vCiqXPmAq6xHrR4emPoYy5-UomtbnUjD?usp=sharing)

### Graph 2

- A cumulative of 97375 Nodes and 482442 edges
- Around 29460 users and 67935 issues

You may find the graphs here: [click here](https://drive.google.com/drive/folders/1vCiqXPmAq6xHrR4emPoYy5-UomtbnUjD?usp=sharing)

### Example Nodes and Edges

## Method

1. Fetch all the closed pull requests of respective repositories
2. Use the pull requests to fetch all the users and issues related to the pull request
3. Connect users across issues using the pull requests
4. Connect users across users using
   - Contributed Repositories
   - Starred Repositories
5. Connect Issues across Issues using
   - Languages
6. Generate connections across unmapped users and unclosed issues

### Repositories

- A list of repositories from github allstars for the year 2021-2022
- Around 2500 repositories used.

### Errors Faced

- Disconnected or sparsely connected nodes will not have predictions.
- Algorithms do not take into account different users, issues, weights.
- The accuracy is generally lower than non-network based prediction.
- Accuracy Measurement is not guaranteeing a correct accuracy prediction.
