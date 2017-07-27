
import tweepy
import logging
import psycopg2
import time

consumer_key = '6WqCLElvMLYiQDnaLtcRMNm5Z'
consumer_token= 'Fh1firIXdBtRCIAYe7ojNjAhkqfP3LYmCzEgixUu2Pu4eyY9Wr'
access_token ='17298291-DoYnEMgJ91RIUFzhfguTeLp53GdiKk9qt162RVSrm'
access_token_secret = 'RLFWzMvbtfhnh8M72ozMxyNLCgFOcrMCJP7IU31T7ka1M'
auth = tweepy.OAuthHandler(consumer_key, consumer_token)
auth.set_access_token(access_token, access_token_secret)

logging.basicConfig(filename='counties.log',  level = logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')



api = tweepy.API(auth)
# API has a 15 minute call interval
interval = 900
def main():
	conn = psycopg2.connect('dbname=twitter_feeds user = postgres password=password')
	cur = conn.cursor()
	county_query = 'select county from counties limit 10;'
	counties = cur.execute(county_query)
	print(counties)
	county = counties.fetchone()
	calls = 0
	while county:
		#search for county results in twitter.
		state_time = time.time()
		if calls < 450:
			cursor = get_search_results(county)
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
						print('Name: ' + name + ' UID: ' + uid + " Screen Name: " + screen_name + ' Location: ' + location)
		else:
			#Need to find out how much time has elapsed between calls and wait until it's reached the 15 minute limit timeframe
			time.sleep(interval - (time.time() - start_time))

				

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