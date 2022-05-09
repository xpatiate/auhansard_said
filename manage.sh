#!/bin/bash

# first arg: 'read' or 'cleanup'
ACTION=$1
# second arg: parlinfo URL for today's Senate Hansard, or "0"
URL_SENATE=$2
# second arg: parlinfo URL for today's House Hansard, or "0"
URL_REPS=$3
# third arg: optional directory in which to copy the downloaded XML files
DATA_COPY=$4
# fourth arg: date of speeches
FILE_DATE=$5

DATA_EXT="data/external"
DATA_INTERIM="data/interim"
DATA_PROC="data/processed"


if [ -z "$FILE_DATE" ]
then
    FILE_DATE=$( date +%Y-%m-%d )
fi
echo $FILE_DATE
FILE_S="${FILE_DATE}-S.xml"
FILE_R="${FILE_DATE}-R.xml"
FILE_P="${FILE_DATE}.txt"
FILE_C="${FILE_DATE}.csv"

if [ "$ACTION" == "-h" ]
then
    echo "manage.sh read|cleanup 'senate_url' 'reps_url' copy_to_dir"
elif [ "$ACTION" == "read" ]
then

    if [ -n "$URL_SENATE" -a "$URL_SENATE" != "0" ]
    then
        echo "Downloading Senate XML from $URL_SENATE to $DATA_EXT/$FILE_S"
        curl -s -o $DATA_EXT/$FILE_S $URL_SENATE
        ls -l $DATA_EXT/$FILE_S && 
            ./extract-speech.py $DATA_EXT/$FILE_S > $DATA_INTERIM/$FILE_S 
        if [ -n "$DATA_COPY" ]
        then
            cp $DATA_EXT/$FILE_S $DATA_COPY
        fi
        ls -l $DATA_INTERIM/$FILE_S
        echo
    fi
    if [ -n "$URL_REPS" -a "$URL_REPS" != "0" ]
    then
        echo "Downloading Reps XML from $URL_REPS to $FILE_R"
        curl -s -o $DATA_EXT/$FILE_R $URL_REPS
        ls -l $DATA_EXT/$FILE_R &&
            ./extract-speech.py $DATA_EXT/$FILE_R > $DATA_INTERIM/$FILE_R
        if [ -n "$DATA_COPY" ]
        then
            cp $DATA_EXT/$FILE_R $DATA_COPY
        fi
        ls -l $DATA_INTERIM/$FILE_R
        echo
    fi

    ./identify_words.py $DATA_INTERIM --csv $DATA_PROC/$FILE_C > $DATA_PROC/$FILE_P

elif [ "$ACTION" == "cleanup" ]
then

    ./identify_words.py $DATA_INTERIM --store \
        && rm $DATA_EXT/*xml \
        && rm $DATA_INTERIM/*xml \
        && rm $DATA_PROC/*txt \
        && rm $DATA_PROC/*csv

fi
