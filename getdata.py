from bs4 import BeautifulSoup
import csv
import Queue
import requests
import sys
from threading import Thread

num_of_threads = 50

senate = "australian_federal_election_2016_-_senate_candidates.txt"
reps = "australian_federal_election_2016_-_house_of_reps_candidates.txt"

file_to_use = reps

if len(sys.argv) > 1:
    if sys.argv[1] == "senate":
        file_to_use = senate
    elif sys.argv[1] == "reps":
        file_to_use = reps

wikiurl = "https://search.wikileaks.org/"

additional_queries = [
        "total",
        "property",
        "tax",
        "corruption",
        "mining",
        "lobbyist",
        "union",
        "fraud",
        "source",
        "leak",
        "opposition",
        "faction",
        "foreign investment",
        "declaration",
        "proposal",
        "donation",
        "incident",
        ]

queuelist = Queue.Queue()

def worker():
    """
    goes and does the actual work of getting data
    """
    while True:
        item = queuelist.get()
        data = get_query_data(item)
        cw.writerow(data)
        queuelist.task_done()

def get_query_data(candidate):
    """
    Takes a candidate's name and does a query on their data
    """

    candidate_data = [candidate]
    zerototal = False

    for query in additional_queries:

        if zerototal is False:
            data = query if query != "total" else ""
            payload = {
                    'q': "%s+%s" % (candidate, data)
            }

            response = requests.get(wikiurl, params=payload)

            soup = BeautifulSoup(response.text, 'html.parser')
            count = int(soup.select("div.total-count span")[0].string.replace(',',''))
        else:
            count = 0

        candidate_data.append(count)

        # we use this so we don't look up additional queries if it isn't
        # needed, we just add a bunch of zeros in there.
        if (query=="total" and count == 0):
            zerototal = True

    return (candidate_data)

# Main section here kicks everything off

cw = csv.writer(sys.stdout)
cw.writerow(["name"] + additional_queries)

f = open(file_to_use, 'r')

# open a stack of threads to try and make this go fast
for i in range(num_of_threads):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

# add the candidates to the queue
for line in f:
    candidate = line.rstrip()
    queuelist.put(candidate)

f.close()

# wait until all the jobs are complete
queuelist.join()

