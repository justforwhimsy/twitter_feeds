
import psycopg2
import tweepy
import logging
import time
import json

#credentials stored in a json file so I don't commit code with sensative data
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

#save logging information to a separate log file
logging.basicConfig(filename='counties.log',  level = logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s')

api = tweepy.API(auth)

# API has a 15 minute call interval
interval = 900

def main():
	conn = psycopg2.connect('dbname=%s user = %s password=%s'% (dbname, dbuser, password))
	cur = conn.cursor()
	county_query ='select distinct(county) from counties;'
	_t = cur.execute(county_query)
	county = cur.fetchone()[0]

	start_time = time.time()
	while county:
		#collect the rate limit statuses to ensure we don't perform too many calls in a given timespan
		rate_status = api.rate_limit_status()
		logging.debug(rate_status)
		rate_limit = rate_status['resources']['application']['/application/rate_limit_status']['remaining']
		search_limit = rate_status['resources']['users']['/users/search']['remaining']
		logging.debug('Rate Limit = ' +str(rate_limit))
		logging.debug('User search limit = ' + str(search_limit))
		
		#if we reached the rate limit, we want to wait sleep through the remainder of the 15 minute window
		if rate_limit == 0 or search_limit == 0:
			tts = interval - (time.time() - start_time)
			logging.info('Call limit reached. Sleeping for ' + str(tts) + " seconds")
			time.sleep(tts + 10)#adding an extra 10 seconds to ensure we don't start early
			start_time = time.time()

		#search for county results in twitter.
		logging.info('Retrieving accounts associated with ' + county)
		cursor = get_search_results(county)
		count = 0
		#run through each section
		for page in cursor:
			if count >= 100:
				break
			for user in page:
				screen_name = user.screen_name
				name = user.name
				uid = user.id_str
				### TODO Collect followers related to a page
				followers = get_followers(uid)
				### Create method for verifyng the location of the feed we searched for and the followers
				#location = get_location(user)
				# for follower in followers:
				location = user.location
				if location != "":
					count +=1
					try:
						logging.debug('Name: ' + name + ' UID: ' + uid + " Screen Name: " + screen_name + ' Location: ' + location)
					except Exception as e:
						logging.error("Something is wrong with the content retrieved for the feed")
						logging.error(e)
		county = cur.fetchone()[0]
	
def get_location(user):
	###TODO
	# parse out location if they have one - This is entered by the user so can vary 
	# check location of tweets if that is enabled
	# 			
def get_followers(uid):
	followers = api.followers_ids(uid)
	return followers

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
