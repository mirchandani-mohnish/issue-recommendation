import multiprocessing
from fin_graph import fin

if __name__ == '__main__':
    # Get the number of available cores
    num_cores = multiprocessing.cpu_count()
    num_cores = 2
    print(f"Number of available cores: {num_cores}")
    # Create a pool of worker processes
    with multiprocessing.Pool(num_cores) as p:
        # Submit tasks to be executed by the worker processes
        orgList = list(set(list(open("data/input/orgList/orgList3.csv", "r"))
                           ).difference(set(list(open("data/input/orgList/orgList2.csv", "r")))))
        orgList = [org.replace('\n', '') for org in orgList]
        orgList.sort(reverse=True)
        # orgList = ['unifyai']

        result = p.map(fin, orgList)
    print(result)