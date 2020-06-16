#!/usr/bin/env python3

import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser("")
parser.add_argument("file", type=str)
args = parser.parse_args()
inputfile = args.file

output = "<session>"
with open(inputfile, "r") as x:
    soup = BeautifulSoup(x, "xml")

    header = soup.find("session.header")
    output += f"{header.chamber}"

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
output += "</session>"
outsoup = BeautifulSoup(output, "xml")
print(outsoup)
