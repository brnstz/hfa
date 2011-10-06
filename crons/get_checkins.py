#!/usr/bin/python

import urllib
import os
import time
import json

CONF = json.load(open('/home/bseitz/git/hfa/conf/hfa.conf'))
ROOT  = CONF['root']
TOKEN = CONF['token']
API   = 'https://api.foursquare.com/v2/venues/%s/herenow?oauth_token=%s&limit=%d&offset=%d&afterTimestamp=%d'

TS_FILE = ROOT + '/data/last_timestamp'
TS_OFFSET = 60

DEFAULT_LIMIT=500

# home_file_code => 4sq venue id
VENUES = CONF['stadiums']

def get_url(venue, afterTimestamp=0, limit=DEFAULT_LIMIT, offset=0):
	return API % (venue, TOKEN, limit, offset, afterTimestamp)

def get_last_ts():
	fh = open(TS_FILE, 'r')
	ts = int(fh.read())
	fh.close()
	
	return ts

def save_ts(ts):
	fh = open(TS_FILE + '.tmp', 'w')
	fh.write(str(ts))
	fh.close()
	os.rename(TS_FILE + '.tmp', TS_FILE)

def run_venues():
	last_ts = get_last_ts()
	ts = int(time.time())

	for hfc in VENUES.keys():
		url = get_url(VENUES[hfc], last_ts - TS_OFFSET)

		# Get data from 4sq
		url_fh  = urllib.urlopen(url)
		data = url_fh.read()
		url_fh.close()
	
		# If need to call multiple times, call it data2.json or whatev
		mydir  = '%s/data/checkins/%d/%s' % (ROOT, ts, hfc)
		myfile = '%s/data.json' % (mydir)
		
		ensure_dir(myfile)

		fh = open(myfile + '.tmp', 'w')
		fh.write(data)
		fh.close()
		os.rename(myfile + '.tmp', myfile)

	save_ts(ts)	

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

run_venues()
