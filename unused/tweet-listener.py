#!/usr/bin/env python3

import os
import tweepy

# Consumer keys and access tokens, used for OAuth
# consumer_key=os.environ.get('CONSUMER_KEY')
# consumer_secret=os.environ.get('CONSUMER_SECRET')
# access_token=os.environ.get('ACCESS_TOKEN')
# access_token_secret=os.environ.get('ACCESS_TOKEN_SECRET')
consumer_key = os.environ.get("CONTEXT_CONSUMER_KEY")
consumer_secret = os.environ.get("CONTEXT_CONSUMER_SECRET")
access_token = os.environ.get("CONTEXT_ACCESS_TOKEN")
access_token_secret = os.environ.get("CONTEXT_ACCESS_TOKEN_SECRET")

print(f"{consumer_key} {consumer_secret} {access_token} {access_token_secret}")

# OAuth process, using the keys and tokens
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
# api = tweepy.API(auth)


class StdOutListener(tweepy.StreamListener):
    """Handles data received from the stream."""

    def on_status(self, status):
        # Prints the text of the tweet
        print("Tweet text: " + status.text)

        return True

    def on_error(self, status_code):
        print("Got an error with status code: " + str(status_code))
        return True  # To continue listening

    def on_timeout(self):
        print("Timeout...")
        return True  # To continue listening


if __name__ == "__main__":
    listener = StdOutListener()
    print(listener)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    print(auth)
    response = auth.set_access_token(access_token, access_token_secret)
    print(response)

    stream = tweepy.Stream(auth, listener)
    print(stream)
    aus_hansard_id = "139904701"
    test_metaphor_id = "575930104"
    stream.filter(follow=[aus_hansard_id, test_metaphor_id])
