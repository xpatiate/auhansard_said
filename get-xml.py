#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup, SoupStrainer
import requests
from urllib.parse import urlparse

parser = argparse.ArgumentParser("")
parser.add_argument("url", type=str)
args = parser.parse_args()
hansard_url = args.url

final_url = ""


def print_url(r, *args, **kwargs):
    final_url = r.url
    print("final url now %s" % final_url)
    return r


# XXX why does certificate show as invalid?
ssl_verify = False
r = requests.get(hansard_url, verify=ssl_verify, hooks={"response": print_url})
final_url = r.url
html_doc = r.text
# print(html_doc)


toc = SoupStrainer(id="documentToc")
soup = BeautifulSoup(html_doc, "html.parser")  # , parse_only=toc)
html_contents = soup.prettify()
target_url = ""
# print(html_contents)

for a in soup.find_all("a"):
    for c in a.contents:
        print(c.string)
        if c.string == "View/Save XML" or c.string == "View XML":
            print(a)
            target_url = a["href"]

if target_url:
    print("final url is %s" % final_url)
    print("target url is %s" % target_url)

    u = urlparse(final_url)
    print(u)
    getxml = "%s://%s%s" % (u.scheme, u.netloc, target_url)
    print("xml url is %s" % getxml)

    # get XML
    x = requests.get(getxml, verify=ssl_verify)
    # get date from XML
    # save XML with date in filename`
