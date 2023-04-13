# Codetriaging: The SNAzzy Way

A project by:

AU2040004 - Priya Jani
AU2040028 - Yansi Memdani
AU2040110 - Mohnish Mirchandani
AU2040241 - Priyanshu Pathak

## Graph Definition

## To run the file

You will need pythone 3.6 or greater
You need to install the following packages. (pip or conda)
pandas
numpy
ijson
matplotlib
networkx

### Nodes

- A cumulative of 10,000 nodes

### Edges

- A cumulative of 8000 edges

## Method

1. Fetch all the closed pull requests of respective repositories
2. Use the pull requests to fetch all the users and issues related to the pull request
3. Connect users across issues using the pull requests
4. Connect users across users using
   - Followers
   - Starred Repositories
5. Connect Issues across Issues using
   - Labels
   - Languages
6. Generate connections across unmapped users and unclosed issues

## Stats

### Repositories

- A list of repositories from github allstars for the year 2021-2022
- Around 2500 repositories used.

### Nodes

### Errors Faced

- Too many edges in graph when connecting issues causing minor values of prediction
