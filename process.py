#!/usr/bin/env python3
"""Read XML files containing Hansard debates and extract words not already seen."""

import argparse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import regex as re
import redis
import xmltodict

parser = argparse.ArgumentParser('Process Hansard XML files')
parser.add_argument('xmldir')
parser.add_argument('--store', action='store_true')
parser.add_argument('--print', action='store_true')
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()
xmldir = args.xmldir
do_store = args.store
do_print = args.print
debug = args.debug

r = redis.StrictRedis()

allwords = {}
stop_words = set(stopwords.words('english'))
house_display = {
    'R': 'House of Representatives',
    'S': 'Senate'
}
emdash = '—'
splitchars = re.compile(r'[-—/]')
filematch = re.compile(r'.+/(\d{4}-\d{2}-\d{2})-([RS]{1}).xml')
skip_word_matches = [
    re.compile(r'\d+'),  # all numbers
    re.compile(r'^[^a-z]+$')  # contains no a-z
]
matchpunct = re.compile(r"\p{P}+")
matchurl = [
    re.compile(r'https?://\S+'),
    re.compile(r'[a-z]+\.[a-z/]+')
]

newwords = {}


def strip_urls(text):
    """Remove any URLs from text."""
    for p in matchurl:
        text = re.sub(p, '', text)
    return text


def remove_punctuation(word):
    """Remove all punctuation chars."""
    return re.sub(matchpunct, "", word)


def skip_word(word):
    """Flag any words that should be skipped."""
    return any([p.match(word) for p in skip_word_matches])


def extract_text(el, house, dateseen, speaker):
    """Parse XML and find speech text."""
    mytext = ''
    if isinstance(el, list):
        for subel in el:
            extract_text(subel, house, dateseen, speaker)
    elif isinstance(el, str):
        mytext = el
    elif isinstance(el, dict) and '#text' in el:
        mytext = el['#text']
    if mytext:
        process_text(mytext, house, dateseen, speaker)


def process_text(text, house, dateseen, speaker):
    """Break a speech up into words, filter and act on new ones."""
    # first strip URLs before they get broken up
    cleaned = strip_urls(text)
    # split into array -> drop stopwords -> split on [-/] -> strip punctuation
    words = [remove_punctuation(s) for w in word_tokenize(cleaned) if w not in stop_words
             for s in re.split(splitchars, w)]
    if debug:
        print(words)
    for word in words:
        checkword = word.lower()
        if not skip_word(word) and checkword not in newwords and not r.get(checkword):
            if do_store:
                r.set(checkword, '%s:%s:%s' % (house, dateseen, speaker))
            else:
                newwords[checkword] = '%s:%s:%s' % (house, dateseen, speaker)
            print("Adding '%s', said by %s in the %s on %s" % (word, speaker, house_display[house], dateseen))


def readfile(xmlfile):
    """Read an XML file and process text."""
    print("reading %s" % xmlfile)
    m = filematch.match(xmlfile)
    if m:
        filedate, house = m.group(1, 2)
        print('date %s, house %s ' % (filedate, house))
        with open(xmlfile, 'r') as x:
            obj = xmltodict.parse(x.read())
            for speech in obj['debates']['speech']:
                speaker = speech.get('@speakername')
                ps = speech.get('p')
                if ps:
                    extract_text(ps, house, filedate, speaker)


# Filenames should be named as [date]-[house].xml e.g. 2018-09-20-R.xml
files = sorted(list(filter(lambda x: x.endswith('xml'), os.listdir(xmldir))))
for xmlfile in files:
    readfile(xmldir + '/' + xmlfile)

if do_print:
    # go through newwords and print any that pass additional criteria
    for word in newwords:
        print(word)
