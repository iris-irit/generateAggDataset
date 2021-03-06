import csv

def lookupTweet(id,json_raw) :
	for j in json_raw :
		if j["id"] == id :
			return j


def get_all_tweets(id, api):
	# Twitter only allows access to a users most recent 3240 tweets with this method


	# initialize a list to hold all the tweepy Tweets
	alltweets = []



	try :

		# make initial request for most recent tweets (200 is the maximum allowed count)
		new_tweets = api.user_timeline(user_id=id, count=200)

		# save most recent tweets
		alltweets.extend(new_tweets)

		# save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		# keep grabbing tweets until there are no tweets left to grab
		while len(new_tweets) > 0:
			print
			"getting tweets before %s" % (oldest)

			# all subsiquent requests use the max_id param to prevent duplicates
			new_tweets = api.user_timeline(user_id=id, count=200, max_id=oldest)

			# save most recent tweets
			alltweets.extend(new_tweets)

			# update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1

			print
			"...%s tweets downloaded so far" % (len(alltweets))

		# transform the tweepy tweets into a 2D array that will populate the csv
		outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]



		return outtweets

	except TypeError :
		return []


def getNbInPeriod(tw,d) :

	year = d.year
	month = d.month

	nb = 0

	for el in tw :
		if el[1].year == year and el[1].month == month :
			nb += 1

	return nb

def decideBetweenZeroAndMax(t,d) :
	if t[1] > d :
		return "max"
	else :
		return 0