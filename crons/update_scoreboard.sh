#!/bin/sh

ROOT="/usr/local/hfa"
#ROOT="/home/bseitz/git/hfa"

YEAR=`date +%Y`
MONTH=`date +%m`
DAY=`date +%d`


# MLB 
SCOREBOARD_URL="http://mlb.mlb.com/gdcross/components/game/mlb/year_$YEAR/month_$MONTH/day_$DAY/master_scoreboard.json"
SCOREBOARD_FILE="$ROOT/static/mlb-scoreboard-$YEAR-$MONTH-$DAY.json"

/usr/bin/curl 2> /dev/null $SCOREBOARD_URL > $SCOREBOARD_FILE.new && mv $SCOREBOARD_FILE.new $SCOREBOARD_FILE

# NFL 
NFL_REGULAR_URL="http://www.nfl.com/liveupdate/scorestrip/ss.xml"
NFL_POST_URL="http://www.nfl.com/liveupdate/scorestrip/postseason/ss.xml"

NFL_REGULAR_FILE="$ROOT/static/nfl-scoreboard-regular-$YEAR-$MONTH-$DAY.xml"
NFL_POST_FILE="$ROOT/static/nfl-scoreboard-post-$YEAR-$MONTH-$DAY.xml"

NFL_FINAL_FILE="$ROOT/static/nfl-scoreboard-$YEAR-$MONTH-$DAY.json"

/usr/bin/curl 2> /dev/null $NFL_REGULAR_URL > $NFL_REGULAR_FILE.new && mv $NFL_REGULAR_FILE.new $NFL_REGULAR_FILE
/usr/bin/curl 2> /dev/null $NFL_POST_URL > $NFL_POST_FILE.new && mv $NFL_POST_FILE.new $NFL_POST_FILE

$ROOT/crons/convert_nfl.py $NFL_REGULAR_FILE $NFL_POST_FILE $NFL_FINAL_FILE
