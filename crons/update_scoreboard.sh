#!/bin/sh

YEAR=`date +%Y`
MONTH=`date +%m`
DAY=`date +%d`

export SCOREBOARD_URL="http://mlb.mlb.com/gdcross/components/game/mlb/year_$YEAR/month_$MONTH/day_$DAY/master_scoreboard.json"
export SCOREBOARD_FILE="/usr/local/hfa/data/static/master_scoreboard-$YEAR-$MONTH-$DAY.json"

/usr/bin/curl 2> /dev/null $SCOREBOARD_URL > $SCOREBOARD_FILE.new && mv $SCOREBOARD_FILE.new $SCOREBOARD_FILE
