#!/usr/bin/env python3

import csv
import os
import random
import sys
import time
import tweepy
import argparse

parser = argparse.ArgumentParser("Read a CSV file and post tweets")
parser.add_argument("csv_path")
parser.add_argument("--delay", action="store_true")
parser.add_argument("--delay-min", type=int)
parser.add_argument("--delay-max", type=int)
args = parser.parse_args()
csv_path = args.csv_path
do_delay = args.delay or args.delay_min or args.delay_max
DELAY_MIN = args.delay_min or 60
DELAY_MAX = args.delay_max or 90

if do_delay:
    print(f"tweeting with min delay {DELAY_MIN} and max delay {DELAY_MAX}")
else:
    print(f"tweeting with no delay")


TWEET_NAME = "@auhansard_said"
# Consumer keys and access tokens, used for OAuth
consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)


# cx_consumer_key = os.environ.get("CONTEXT_CONSUMER_KEY")
# cx_consumer_secret = os.environ.get("CONTEXT_CONSUMER_SECRET")
# cx_access_token = os.environ.get("CONTEXT_ACCESS_TOKEN")
# cx_access_token_secret = os.environ.get("CONTEXT_ACCESS_TOKEN_SECRET")
# print(
#    f"1 {cx_consumer_key} 2 {cx_consumer_secret} 3 {cx_access_token} 4 {cx_access_token_secret}"
# )
# OAuth process, using the keys and tokens
# cx_auth = tweepy.OAuthHandler(cx_consumer_key, cx_consumer_secret)
# cx_auth.set_access_token(cx_access_token, cx_access_token_secret)

# Creation of the actual interface, using authentication
# cx_api = tweepy.API(cx_auth)
# print(cx_api.me())

# cx_api.update_status(f"testing {random.randint(0,100)}")
# sys.exit()

# read CSV file
with open(csv_path) as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        word = row[0]
        context = row[1]

        # post each word as a single tweet
        tw_response = api.update_status(word)
        print(f"{word} {tw_response.id}")

        # use this ID as second arg to `update_status` to send a reply as saidby
        # include TWEET_NAME in the status message

        # use main account API rather than context while in twitter jail
        api.update_status(f"{TWEET_NAME} {context}", tw_response.id)
        # cx_api.update_status(f"{TWEET_NAME} {context}", tw_response.id)
        if do_delay:
            time.sleep(random.randint(DELAY_MIN, DELAY_MAX))

# https://tweepy.readthedocs.io/en/latest/api.html
