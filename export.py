#!/usr/bin/env python3
"""Write contents of redis db to a CSV file."""

import csv
import redis

r = redis.StrictRedis()

with open('wordlist.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)

    # for each a..z
    for char in list(map(chr, range(97, 123))):
        # get all keys beginning with char
        words = r.keys('%s*' % char)
        print('%s %s' % (char, len(words)))
        for w in words:
            row = [w.decode()]
            row.extend(r.get(w).decode().split(':'))
            csvwriter.writerow(row)
