#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser("")
parser.add_argument("file", type=str)
args = parser.parse_args()
inputfile = args.file

output = ""
with open(inputfile, "r") as x:
    soup = BeautifulSoup(x, "xml")

    # print(soup.find_all("span"))
    # print(soup.get_text())

    # for p in soup.find_all('p'):
    #    print(p.get_text())

    output += "<debates>"
    for debate in soup.find_all("debate"):
        speeches = debate.find_all(["speech", "question", "interjection", "continue"])
        for s in speeches:
            metadata = s.find("talker")
            # print(metadata)
            speaker = metadata.find("name").text
            output += '<speech speakername="%s">' % speaker
            content = s.find("talk.text")
            for p in content.find_all("p"):
                output += "<p>%s</p>" % p.get_text()
            output += "</speech>"
    output += "</debates>"

outsoup = BeautifulSoup(output, "xml")
# print(outsoup.decode(formatter='xml'))
print(str(outsoup))
