#!/usr/bin/python

import sys
import elementtree.ElementTree
import pprint
import json
import os

# FIXME
CONF = json.load(open('/usr/local/hfa/conf/hfa.conf'))
#CONF = json.load(open('/home/bseitz/git/hfa/conf/hfa.conf'))
ROOT = CONF['root']

files = sys.argv[1:-1]

def read_file(file):
    tree = elementtree.ElementTree.parse(file)
    games = tree.find('gms').findall('g')
    parsed_games = {}

    for game in games:
        eid = game.attrib['eid']
        start_date = '-'.join((eid[0:4], eid[4:6], eid[6:8]))

        start_time = game.attrib['t']
        home_team  = game.attrib['h'].lower()
        away_team  = game.attrib['v'].lower()

        games_today = parsed_games.get(start_date, [])
        games_today.append({
            "start_date": start_date,
            "start_time": start_time,
            "home_team": home_team,
            "away_team": away_team
        })

        parsed_games[start_date] = games_today

    return parsed_games

def read_all_files(files):
    all_parsed_games = {}
    for file in files:
        new_parsed_games = read_file(file)
        all_parsed_games.update(new_parsed_games)

    for date in all_parsed_games:
        games = all_parsed_games[date]
        write_filename = os.path.join(
            ROOT, "static/", "nfl-scoreboard-" + date + ".json"
        )
        fh = open(write_filename + '.tmp', 'w')
        fh.write(json.dumps({"games": games}))
        fh.close()
        os.rename(write_filename + ".tmp", write_filename)

read_all_files(files)
