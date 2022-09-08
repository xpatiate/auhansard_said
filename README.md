# AUhansard_said

A collection of scripts used in producing the `AUhansard_said` Twitter feed, which posts a notification every time a new word is used in Hansard debates in the Australian parliament. Some data comes from data.openaustralia.org.au which goes back to 2006 so "new" means "unused since 2006".

This is a WIP and some manual processes are still involved in posting notifications, improvements are underway.

# Current process

* tweet-listener prints notification of every AUS_Hansard tweet
* get-xml is supposed to take URL from tweet and download XML
* extract-speech reads the orig XML and outputs a simplified version
* process.py reads the simplified XML and prints new words
* tweet-poster.py posts the tweets

Manual steps in process:
* TODO: run tweet-listener.py for notifications, have it run get-xml.py
* for now: watch @AUS_Hansard for 'full transcript' links on sitting days (usually around 10.30-11pm)
* go to link, view XML, copy urls for Senate and Reps
* run `manage.sh read "senate-url" "reps-url"`
* edit the CSV file in data/processed
* make sure access token env vars are exported in shell
* run `tweet-poster.py data/processed/[date].csv`
* run `manage.sh cleanup`

### TODO:

* backfill database with archived Hansards up to 1980 from https://github.com/wragge/hansard-xml
* figure out how to get 1980-2006
* improve scraping to require less manual intervention
* improve detection of proper names, place names, brand names etc
* better handling of interjections/other speakers
* investigate detecting novel bigrams
