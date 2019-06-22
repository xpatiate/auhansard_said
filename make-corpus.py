#!/usr/bin/env python3

import argparse
from nltk.corpus import stopwords
import json
import os
from nltk.tokenize import word_tokenize
import xmltodict

parser = argparse.ArgumentParser('Process Hansard XML files')
parser.add_argument('indir')
parser.add_argument('outdir')
args = parser.parse_args()
indir = args.indir
outdir = args.outdir

stop_words = set(stopwords.words('english'))

def process_text(speech):
    return [t.lower() for t in word_tokenize(speech) if t.isalpha() and t not in stop_words]

def extract_text(el):
    """Parse XML and find speech text."""
    mytext = ''
    if isinstance(el, list):
        for subel in el:
            extract_text(subel)
    elif isinstance(el, str):
        mytext = el
    elif isinstance(el, dict) and '#text' in el:
        mytext = el['#text']
    if mytext:
        return process_text(mytext)

def parsefile(infile, outfile):
    with open(infile,'r') as x:
        allparas = []
        obj = xmltodict.parse(x.read())
        for speech in obj['debates']['speech']:
            ps = speech.get('p')
            wordlist = extract_text(ps)
            if wordlist:
                allparas.append(wordlist)
        with open(outfile,'w') as w:
            w.write(json.dumps(allparas))

# Filenames should be named as [date]-[house].xml e.g. 2018-09-20-R.xml
files = sorted(list(filter(lambda x: x.endswith('xml'), os.listdir(indir))))
for xmlfile in files:
    jsonfile = outdir + '/' + xmlfile.replace('xml','json')
    parsefile(indir + '/' + xmlfile, jsonfile)
