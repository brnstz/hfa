#!/usr/bin/python

import json
import pymongo
import sys
import time
import pprint
import fanutil

# FIXME
CONF_FILE = '/home/bseitz/git/hfa/conf/hfa.conf'
#CONF_FILE = '/usr/local/hfa/conf/hfa.conf'

class FanData:
    def __init__(self):
        self.conf = json.load(open(CONF_FILE))
        self.db   = pymongo.Connection()[self.conf['db']]
    
    def get_venue_id(self, sport, team):
        return self.conf['sports'][sport]['stadiums'][team]

    def count_all_checkins(self, sport, team):
        venue_id = self.get_venue_id(sport, team)
        return self.db.checkins.find({"venue_id": venue_id}).count()

    def count_all_checkins_by_date(self, sport, team, date_string):
        (date_low, date_high) = fanutil.date_string_to_dayrange(date_string)
        venue_id = self.get_venue_id(sport, team)

        count = self.db.checkins.find({
            "venue_id":  venue_id,
            "createdAt": {"$gte": date_low, "$lte": date_high}
        }).count()

        print count


        
obj = FanData()
#pprint.pprint(obj.count_all_checkins(sys.argv[1], sys.argv[2]))
obj.count_all_checkins_by_date('nfl', 'gb', '2012-01-15')
