
import psycopg2
import tweepy
import logging
import time
import json

with open('credentials.json') as json_creds:
	d = json.load(json_creds)
	consumer_key = d['twitter']['consumer_key']
	consumer_token= d['twitter']['consumer_token']
	access_token =d['twitter']['access_token']
	access_token_secret = d['twitter']['access_token_secret']
	dbname= d['db']['db']
	user = d['db']['user']
	password = d['db']['password']

auth = tweepy.OAuthHandler(consumer_key, consumer_token)
auth.set_access_token(access_token, access_token_secret)

logging.basicConfig(filename='counties.log',  level = logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')



api = tweepy.API(auth)
# API has a 15 minute call interval
interval = 900
rate_limit = 80
def main():
	conn = psycopg2.connect('dbname=twitter_feeds user = postgres password=password')
	cur = conn.cursor()
	county_query ='select distinct(county) from counties;'
	_t = cur.execute(county_query)
	# county = counties.fetchone()
	calls = 0
	county = cur.fetchone()[0]
	while county:
		#search for county results in twitter.
		print(county)
		start_time = time.time()
		print(str(calls) + "calls made")
		if calls == (rate_limit - 1):
			print('450 call limit reached. Sleeping')
			tts = interval - (time.time() - start_time)
			print('Sleeping for ' + str(tts) + " seconds")
			time.sleep(interval - (time.time() - start_time))

		cursor = get_search_results(county)
		calls +=1
		count = 0
		for page in cursor:
			if count >= 100:
				break
			for user in page:
				screen_name = user.screen_name
				name = user.name
				uid = user.id_str
				location = user.location
				if location != "":
					count +=1
					try:
						print('Name: ' + name + ' UID: ' + uid + " Screen Name: " + screen_name + ' Location: ' + location)
					except:
						print("There's some hinky  encoding here")
		print(str(count))
		county = cur.fetchone()[0]
				

def get_search_results(query):
	cursor = tweepy.Cursor(api.search_users,q =query).pages(10)
	return cursor

def query_db(query):
	_t = db.query(query)
	results =db.use_results()
	return
def insert_feed(uid, screen_name, lang, page_state, verified_county, search_county):

    query = '''INSERT IGNORE INTO twitter_feeds (uid, name, page_state, verified_county, search_county, user_name) VALUES("%s","%s","%s","%s","%s","%s")''' % (uid, name, page_state, verified_county, search_county, screen_name)
    logging.debug("Query: " + query)
    r = db.query(query)
    logging.debug("Query results: " + r)
if __name__ == "__main__":
	main()
