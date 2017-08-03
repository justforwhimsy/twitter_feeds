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

api = tweepy.API(auth)

start = api.rate_limit_status()
tweets = api.reverse_geocode(40.81,
					-73.04,
					100,
					'neighborhood',
					200)
for tweet in tweets:
	print(tweet)
print(start)
end = api.rate_limit_status()
print(end)
base_url = 'https://api.twitter.com/1.1/'
requests.get(base_url + 'search/tweets.json')
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

#Connection to the counties table to test connection and retrieval
# conn = psycopg2.connect('dbname=%s user = %s password=%s' % (dbname, dbuser, password))

# cur = conn.cursor()

# cur.execute('select distinct(county) from counties;')
# result = cur.fetchone()
# count = 1
# while result:
# 	print(result[0])
# 	result = cur.fetchone()
# 	count+= 1
# print(count)

# print(psycopg2.__file__)

