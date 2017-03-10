import pprint
import sys
from datetime import datetime
import pandas as pd
import numpy as np

def getDate(json):

	for doc in json :
		pprint.pprint(doc)

		d = datetime.strptime(doc["created_at"], '%a %b %d %H:%M:%S %z %Y')
		print(d.strftime('%Y-%m-%d at %H'))
		sys.exit()

def findBin(id,l):

	for i in range(1,len(l)):
		if id >= l[i-1] and id <= l[i] :
			return (i-1)


def getHistogram(json):

	hist = {}
	dictTwHour = {}
	dictHourId = {}
	sumBin = {}
	mapTweetBin = {}
	res = {}

	nbTweets = len(json)

	for doc in json :
		#pprint.pprint(doc)

		d = datetime.strptime(doc["created_at"], '%a %b %d %H:%M:%S %z %Y')
		print(d.strftime('%Y-%m-%d at %H:%M'))

		key = str(d.day)+"_"+str(d.hour)+"_"+d.strftime("%M")
		hist.setdefault(key,0)
		hist[key] += 1
		dictTwHour[doc["id"]] = key

	df = pd.DataFrame(columns=["id","time","count"])
	i = 0
	for k in sorted(hist):
		df.loc[i] = [i,k,hist[k]]
		dictHourId[k] = i
		i += 1

	# Bin the data frame by "a" with 10 bins...
	bins = np.linspace(df.id.min(), df.id.max(), 11)

	for idTw in dictTwHour :
		id = dictHourId[dictTwHour[idTw]]
		bin = findBin(id,bins)

		mapTweetBin[idTw] = bin
		sumBin.setdefault(bin,0)
		sumBin[bin] += 1

	for idTw in dictTwHour :
		res[idTw] =  sumBin[mapTweetBin[idTw]] /nbTweets

	return res
