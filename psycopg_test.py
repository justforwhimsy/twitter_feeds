import psycopg2

import time
import requests
import json
import tweepy
import difflib
with open('credentials.json') as json_creds:
	d = json.load(json_creds)
	consumer_key = d['twitter']['consumer_key']
	consumer_token= d['twitter']['consumer_token']
	access_token =d['twitter']['access_token']
	access_token_secret = d['twitter']['access_token_secret']
	dbname= d['db']['db']
	dbuser = d['db']['user']
	password = d['db']['password']

auth = tweepy.OAuthHandler(consumer_key, consumer_token)
auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)

# start = api.rate_limit_status()
# if "': 0" in start:
# 	print('Rate reached for something`')
# tweets = api.reverse_geocode(40.81,
# 					-73.04,
# 					100,
# 					'neighborhood',
# 					200)
# for tweet in tweets:
# 	print(tweet)

### Collect Followers for my user based on the ID ###
# me = api.me()

# print(me)
# str_id = me.id_str
# followers = api.followers_ids(str_id)
# for f in followers:
# 	print(f)
# end = api.rate_limit_status()
# base_url = 'https://api.twitter.com/1.1/'
# requests.get(base_url + 'search/tweets.json')

### Check to see how time works ###
# Check interval timing
# start_time = time.time()
# print(str(start_time))
# time.sleep(60)
# finish_time = time.time()
# print(str(finish_time))
# interval = finish_time - start_time
# print(str(interval))

# Check Twitter connection
# r = requests.get('')

### Connection to the counties table to test connection and retrieval ###
conn = psycopg2.connect('dbname=%s user = %s password=%s' % (dbname, dbuser, password))

cur = conn.cursor()

query = """SELECT DISTINCT(county) FROM counties WHERE state ilike '%s' AND (primary_city ilike '%s' OR acceptable_cities ilike '%%%s%%')""" % ('OR', 'Portland', 'Portland')
print(query)
#query = 'select distinct(county) from counties;'
cur.execute(query)
result = cur.fetchone()
count = 0
while result:
	count+= 1
	print(result[0])
	result = cur.fetchone()
print(count)

# print(psycopg2.__file__)

