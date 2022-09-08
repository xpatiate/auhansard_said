#!/usr/bin/env python3
"""Look at OpenAustralia data site for new files."""

import argparse
import redis
import requests
import os
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser("Process Hansard XML files")
parser.add_argument("outputdir")
args = parser.parse_args()

output_dir = args.outputdir
r = redis.StrictRedis()

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

url = "http://data.openaustralia.org.au/scrapedxml"
index_paths = {"reps": "representatives_debates", "senate": "senate_debates"}
index_qs = "?C=N;O=A"  # ensure we get files in the right order
date_key = "__date"
latest = r.get(date_key).decode() if r.get(date_key) else "2006-01-01"


unseen = []
for house, index_path in index_paths.items():
    index_url = "%s/%s/%s" % (url, index_path, index_qs)
    print("checking %s index: %s" % (house, index_url))
    page = requests.get(index_url)
    soup = BeautifulSoup(page.content, "html.parser")
    files = [a.get_text() for a in soup.find_all("a")]
    for filename in files:
        if not filename.startswith("20"):
            continue
        fdate = filename[:-4]  # drop the .xml suffix
        if fdate <= latest:
            continue
        furl = "%s/%s/%s" % (url, index_path, filename)
        print(furl)
        # get file and write to temp dir
        xmlfile = requests.get(furl)
        outfile = "%s/%s-%s.xml" % (output_dir, fdate, house.upper()[0])
        with open(outfile, "w") as xmlout:
            xmlout.write(xmlfile.text)
        unseen.append(outfile)

if unseen:
    print("The following new files have been downloaded:")
    for xml in unseen:
        print("* %s" % xml)
