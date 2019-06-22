# AUhansard_said

A collection of scripts used in producing the `AUhansard_said` Twitter feed, which posts a notification every time a new word is used in Hansard debates in the Australian parliament. Data comes from data.openaustralia.org.au which goes back to 2006 so "new" means "unused since 2006".

This is a WIP and some manual processes are still involved in posting notifications, improvements are underway.

# Current process

* tweet-listener prints notification of every AUS_Hansard tweet
* get-xml is supposed to take URL from tweet and download XML
* extract-speech reads the orig XML and outputs a simplified version
* process.py reads the simplified XML and prints new words

Manual steps in process:
* TODO: run tweet-listener.py for notifications, have it run get-xml.py
* for now: watch AUS_Hansard for 'full transcript' links on sitting days (usually around 10.30-11pm)
* go to link, view XML, download and save as data/external/YYYY-MM-DD-[RS].xml 
* run extract-speech.py data/external/YYYY-MM-DD-[RS].xml > data/interim/YYYY-MM-DD-[RS].xml to convert to simpler XML format
* once both R & S (if applicable) are in the `interim` dir, run `process.py data/interim` to print out new words and context
* redirect output of process.py into a text file e.g. `data/processed/YYYY-MM-DD.txt`
* run process.py again  with additional `--store` arg to save the new words
* TODO: run scripts to tweet new words and context replies
