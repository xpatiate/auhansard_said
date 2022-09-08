# auhansard_said

A collection of scripts used in producing the `@auhansard_said` Twitter feed, which posts a tweet every time a new word is used in Hansard debates in the Australian parliament. The "newness" of words is determined by comparison against a Redis database, which was originally populated with Hansard transcripts from data.openaustralia.org.au. This data goes back to 2006 so "new" means "unused since 2006".

Proper nouns and obvious typos are excluded, but otherwise any word that hasn't appeared since 2006 is considered tweet-worthy, including different grammatical forms of words that have been previously used.

Only words used in speeches within the House of Representatives and Senate are included, committee transcripts are not.

This project is a WIP and only partially automated - some manual processes are still involved in scraping and analysing transcripts and posting tweets.

## Current process

The following directories are used by the `manage.sh` script:
```
data/external
data/interim
data/processed
```
Run `manage.sh mkdir` to create them.

* Watch @AUS_Hansard for transcript links on sitting days (usually partial transcripts from early afternoon with a final version around 10.30-11pm)
* Run the `manage.sh` bash script with the following arguments:
 * `read` to download and analyse transcripts
 * URL for the latest Senate transcript XML link (or "0" if no Senate transcript available)
 * URL for the latest House of Reps transcript XML link (or "0" if no House transcript available)
 * (optional) directory into which the downloaded transcript should be copied
 * (optional) date of the transcript file (defaults to current date)
* The bash script will:
 * download (and optionally save a copy of) the specified transcripts) to data/external
 * run `extract-speech.py data/external/YYYY-MM-DD-[RS].xml > data/interim/YYYY-MM-DD-[RS].xml` to convert to a simpler XML format
 * run `identify_words.py data/interim` to detect new words, and write them (plus context) into a CSV file in `data/processed`
* Manually review the CSV file, remove proper nouns and typos, remove linebreaks and malformed context 
* Export environment variables with Twitter account credentials
* Run `tweet-poster.py data/processed/YYYY-MM-DD.csv --delay` to post tweets with a randomised delay
* Run `manage.sh cleanup` to remove data files and store tweeted words in the database.

## TODO

* Improve text analysis to exclude proper nouns
* Improve manage.sh or tweet-listener.py to retrieve XML file from links in tweet
* backfill database with archived Hansards up to 1980 from https://github.com/wragge/hansard-xml
* figure out how to get 1980-2006
* improve scraping to require less manual intervention
* improve detection of proper names, place names, brand names etc
* better handling of interjections/other speakers
* investigate detecting novel bigrams
