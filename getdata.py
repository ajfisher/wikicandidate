from bs4 import BeautifulSoup
import csv
import requests
import sys

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

cw = csv.writer(sys.stdout)
cw.writerow(["name"] + additional_queries)

f = open(file_to_use, 'r')

for line in f:
    candidate = line.rstrip()
    candidate_data = [candidate]
    for query in additional_queries:

        data = query if query != "total" else ""
        payload = {
                'q': "%s+%s" % (candidate, data)
        }

        response = requests.get(wikiurl, params=payload)

        soup = BeautifulSoup(response.text, 'html.parser')
        count = int(soup.select("div.total-count span")[0].string.replace(',',''))

        candidate_data.append(count)

    cw.writerow(candidate_data)

