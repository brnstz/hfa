#!/usr/bin/python

import json
import os
import re
import datetime

TODAY = datetime.date.today()

CONF = json.load(open('/usr/local/hfa/conf/hfa.conf'))

DATA_DIR = "%s/data/checkins" % (CONF['root'])

MATCH_DATA = {}

# Hash of most popular cities
CITY_COUNT = {}

def game_matchups():
	fh = open(os.path.join(CONF['root'], 'data/static/master_scoreboard-' + TODAY.isoformat() + '.json'), 'r')
	data = json.loads(fh.read())
	fh.close()

	home_to_away = {}
	for game in data['data']['games']['game']:
		home_to_away[game['home_file_code']] = game['away_file_code']

	return home_to_away

HOME_TO_AWAY = game_matchups()

def do_file_code_match(file_code, row):
	for regex in CONF['file_code_match'][file_code]:
		city = row['user']['homeCity']

		if city in CITY_COUNT:
			CITY_COUNT[city] += 1
		else:
			CITY_COUNT[city] = 1

		if re.search(regex, city, flags=re.IGNORECASE):
			return True

def run_one_venue(dirname, home_file_code):
	# FIXME: allow multiple data files

	fh = open(os.path.join(dirname, 'data.json'), 'r')
	data = json.loads(fh.read())
	fh.close()

	# If can't find away file code, there is no game scheduled
	# at the home_file_code today. Someone is checked in for no 
	# reason :)
	away_file_code = HOME_TO_AWAY.get(home_file_code, None)

	if away_file_code == None:
		return
	
	# Init file codes if needed
	if MATCH_DATA.get(home_file_code, None) == None:
		MATCH_DATA[home_file_code] = {}

	if MATCH_DATA.get(away_file_code, None) == None:
		MATCH_DATA[away_file_code] = {}
	
	if MATCH_DATA.get(home_file_code + '_other', None) == None:
		MATCH_DATA[home_file_code + '_other'] = {}

	for row in data['response']['hereNow']['items']:
		declared_code = get_declared_code(row)

		if home_file_code == declared_code:
			MATCH_DATA[home_file_code][row['id']] = row
		elif away_file_code == declared_code:
			MATCH_DATA[away_file_code][row['id']] = row
		elif do_file_code_match(home_file_code, row):
			MATCH_DATA[home_file_code][row['id']] = row
		elif do_file_code_match(away_file_code, row):
			MATCH_DATA[away_file_code][row['id']] = row
		else:
			MATCH_DATA[home_file_code + '_other'][row['id']] = row

def get_declared_code(row):
	user_id_int = int(row['user']['id'])
	declare_file = os.path.join(CONF['root'], 'data/declare', str(user_id_int % 997), row['user']['id'] + '.json')

	try:
		if os.path.exists(declare_file):
			fh = open(declare_file, 'r')
			data = json.loads(fh.read())
			fh.close()
			team = data.get('team', None)
			return team
		else:
			return None
	except Exception:
		return None


def run_one_ts_dir(dirname):
	for venue_dir in os.listdir(dirname):
		run_one_venue(os.path.join(dirname, venue_dir), venue_dir)
	
def run_all_stats():
	for ts_dir in os.listdir(DATA_DIR):
		if TODAY == datetime.date.fromtimestamp(int(ts_dir)):
			if os.path.isdir(os.path.join(DATA_DIR, ts_dir)):
				run_one_ts_dir(os.path.join(DATA_DIR, ts_dir))

	final_data = {}
	#top_cities = sorted(CITY_COUNT, key=CITY_COUNT.__getitem__, reverse=True)

	for file_code in MATCH_DATA.keys():
		final_data[file_code] = {
			"items": MATCH_DATA[file_code].values(),
			"count": len(MATCH_DATA[file_code]),
			#"top_cities": top_cities[:10]
		}

	

	write_stats(final_data)

def write_stats(final_data):
	filename = os.path.join(CONF['root'], 'data/counts/current-' + TODAY.isoformat() + '.json')
	fh = open(filename + '.tmp', 'w')
	fh.write(json.dumps(final_data))
	fh.close()
	os.rename(filename + '.tmp', filename)
	
run_all_stats()
