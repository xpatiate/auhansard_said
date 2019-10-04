#!/usr/bin/env python3
"""Read XML files containing Hansard debates and extract words not already seen."""

import argparse
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import os
import regex as re
import redis
import xmltodict

parser = argparse.ArgumentParser('Process Hansard XML files')
parser.add_argument('xmldir')
parser.add_argument('--store', action='store_true')
parser.add_argument('--print', action='store_true')
parser.add_argument('--debug', action='store_true')
parser.add_argument('--csv', action='store', default=None, required=False)

args = parser.parse_args()
xmldir = args.xmldir
do_store = args.store
do_print = args.print
debug = args.debug
csv_path = args.csv

r = redis.StrictRedis()

date_key = '__date'
latest = r.get(date_key).decode() if r.get(date_key) else '2006-01-01'

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
tweet_len = 280

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


def extract_text(el, house, dateseen, speaker, csv_writer=None):
    """Parse XML and find speech text."""
    mytext = ''
    if isinstance(el, list):
        for subel in el:
            extract_text(subel, house, dateseen, speaker, csv_writer)
    elif isinstance(el, str):
        mytext = el
    elif isinstance(el, dict) and '#text' in el:
        mytext = el['#text']
    if mytext:
        process_text(mytext, house, dateseen, speaker, csv_writer)


def process_text(text, house, dateseen, speaker, csv_writer):
    """Break a speech up into words, filter and act on new ones."""
    sentences = sent_tokenize(text)

    for sentence in sentences:
        # first strip URLs before they get broken up
        cleaned = strip_urls(sentence)
        # split into array -> drop stopwords -> split on [-/] -> strip punctuation
        words = [remove_punctuation(s) for w in word_tokenize(sentence) if w not in stop_words
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
                print(word)
                # split text by sentence, take first sentence with word in it, check case-insensitive
                # if sentence too long for a tweet, reduce chars from start and end
                show_sentence = sentence
                saidby = "%s in the %s on %s: " % (speaker, house_display[house], dateseen,)
                # Space available for the sentence is the length of a tweet, minus the length of the 'said by' bit, minus 6 chars for pre and post ellipses
                context_len = tweet_len - len(saidby) - 6
                diff_sentence = len(sentence) - context_len
                pre = ''
                post = ''
                # If whole sentence within max length, show whole thing
                if (diff_sentence > 0):
                    chunk = int(diff_sentence / 2)
                    loc = sentence.find(word)
                    start = 0
                    end = 0
                    # go from the start of the sentence
                    if (loc < context_len/2):
                        start = 0
                        end = context_len
                        post = '...'
                    # go until the end of the sentence
                    elif (loc > diff_sentence):
                        start = diff_sentence
                        end = len(sentence)
                        pre = '...'
                    # take a chunk from the middle of the sentence
                    else:
                        start = int(loc - context_len/2)
                        end = start + context_len
                        pre = post = '...'
                    show_sentence = pre + sentence[start:end] + post
                context_tweet = saidby + show_sentence
                print(context_tweet)
                if csv_writer:
                    print(f"writeing [{word}] and [{context_tweet}] to CSV {csv_writer}")
                    response = csv_writer.writerow([word, context_tweet])
                    print(response)


def readfile(xmlfile, latest, csv_writer):
    """Read an XML file and process text."""
    print("reading %s" % xmlfile)
    m = filematch.match(xmlfile)
    if m:
        filedate, house = m.group(1, 2)
        print('date %s, house %s ' % (filedate, house))
        if filedate > latest:
            r.set(date_key, filedate)
            latest = filedate
        with open(xmlfile, 'r') as x:
            obj = xmltodict.parse(x.read())
            for speech in obj['debates']['speech']:
                speaker = speech.get('@speakername')
                ps = speech.get('p')
                if ps:
                    extract_text(ps, house, filedate, speaker, csv_writer)

csv_file = None
csv_writer = None
if csv_path:
    print(f"GOT CSV PATH {csv_path}, opening writer")
    csv_file = open(csv_path,'w')
    csv_writer = csv.writer(csv_file)


# Filenames should be named as [date]-[house].xml e.g. 2018-09-20-R.xml
files = sorted(list(filter(lambda x: x.endswith('xml'), os.listdir(xmldir))))
for xmlfile in files:
    readfile(xmldir + '/' + xmlfile, latest, csv_writer)

if do_print:
    # go through newwords and print any that pass additional criteria
    for word in newwords:
        print(word)

if csv_file:
    csv_file.close()
