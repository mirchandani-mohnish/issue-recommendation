# Codetriaging: The SNAzzy Way

A project by:

AU2040004 - Priya Jani
AU2040028 - Yansi Memdani
AU2040110 - Mohnish Mirchandani
AU2040241 - Priyanshu Pathak

## How to run the code

### Requirements

- Python >=v3.4
- Pandas == 1.5.3
- networkx == 3.0
- matplotlib == 3.6.3
- numpy == 1.23.5

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
- Prognostic Techniques for Graph-Based Link Prediction ( Self-Developed Algorithm )

Each of the files are isolated ipynb files which can be run and tested.

## Methodology

### Data Collection

A considerable amount of time went in data collection specifically because of first-hand data collection for the project. The same was done using the currently presented github api. Additionally, Github API had a limit of 1000 queries per hour for personal users. The following data was collected for the project

- A set of Issues
- A set of Users
- A set of Pull Requests
- The Languages of each issue
- The Contributions of Each User
- The

## Graphs

The code has majorly been tested on two graphs of similar configurations but varying scales. The configuration of our graphs is as follows:

**Nodes (types)**: User, Issue
**Edges**:

- User --- User -> Commonly Contributed Repositories
- User --- User -> Commonly Starred Repositories
- User --- Issue -> Contribution
- Issue --- Issue -> Common Languages of Parent Repository

### Graph 1

- A cumulative of 11000 Nodes and 291375 edges
- Around 3000 users and 8000 issues

### Graph 2

- A cumulative of 92000 Nodes and \_\_\_\_ edges
- Around \_**\_ users and \_\_** issues

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

-
- Too many edges in graph when connecting issues causing minor values of prediction
- Possibility of correlation between language not
