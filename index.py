#!/usr/bin/python

import os
import web
import warnings
import pprint
import sys
import json
import datetime
import urllib

CONF  = json.load(open('/usr/local/hfa/conf/hfa.conf'))
TODAY = datetime.date.today()
ROOT  = CONF['root']
TOKEN = CONF['token']

USER_QUERY='https://api.foursquare.com/v2/users/self?oauth_token='

URLS = (
	'/scoreboard.jsonp', 'Scoreboard',
	'/declare.jsonp', 'Declare',
)


DELETE_KEYS = ['broadcast', 'away_probable_pitcher', 'home_probable_pitcher', 'game_media', 'links', 'video_thumbnail']

def get_scoreboard_file(datestamp):
	return ROOT + '/data/static/master_scoreboard-' + datestamp + '.json'

def get_counts_file(datestamp):
	return ROOT + '/data/counts/current-' + datestamp + '.json'

class Scoreboard:
	def GET(self):
		i = web.input(date=TODAY.isoformat())
		
		counts = load_json(get_counts_file(i.date))
		scoreboard = load_json(get_scoreboard_file(i.date))

		total_checkins = 0

		# If not a list, make it so 
		if not isinstance(scoreboard['data']['games']['game'], (list)):
			scoreboard['data']['games']['game'] = [scoreboard['data']['games']['game']]
		
		for game in scoreboard['data']['games']['game']:
			home = game['home_file_code']
			away = game['away_file_code']

			game['hfa_data'] = {
				'home' : counts.get(home, None),
				'away' : counts.get(away, None),
				'other': counts.get(home + '_other', None)
			}

			for place in ['home', 'away', 'other']:
				total_checkins += game['hfa_data'][place]['count']

			for key in DELETE_KEYS:
				if game.get(key, None):
					del game[key]

		scoreboard['TODAY'] = i.date
		scoreboard['data']['total_checkins'] = total_checkins

		scoreboard['test']['brian'] = 'hey'


		return i.callback + '(' + json.dumps(scoreboard) + ')'

class Declare:
	def GET(self):
		i = web.input(access_token=None, team=None, callback=None)

		if not (i.access_token and i.team):
			return json.dumps({"error" : "No access_token or team"})

		url_fh = urllib.urlopen(USER_QUERY + i.access_token)
		data = url_fh.read()
		url_fh.close()

		obj = json.loads(data)
		user_id = int(obj['response']['user']['id'])
		
		team_data = json.dumps({"user_id" : user_id, "team" : i.team})

		myfile = os.path.join(ROOT, "data/declare/", str(user_id % 997), str(user_id) + '.json')
		ensure_dir(myfile)
		fh = open(myfile + '.tmp', 'w')
		fh.write(team_data)
		fh.close()
		os.chmod(myfile + '.tmp', 0777)
		os.rename(myfile + '.tmp', myfile)

		web.setcookie('team', i.team)
		if i.callback:
			return i.callback + '(' + team_data + ')'
		else:
			return team_data


def touch(fname, times = None):
    with file(fname, 'a'):
	        os.utime(fname, times)

def load_json(filename):
	fh = open(filename, 'r')
	text = fh.read()
	json_obj = json.loads(text)
	fh.close()
	return json_obj

def do_jsonp(callback, filename):
		fh = open(filename, 'r')
		text = fh.read()
		fh.close()
		return callback + '(' + text + ')'

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d, 0777)
        os.chmod(d, 0777)

if __name__ == "__main__":
    warnings.filterwarnings('ignore', 'tempnam', RuntimeWarning)
    app = web.application(URLS, globals())
    app.run()
