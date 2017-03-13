import pprint
import sys
from datetime import datetime, timedelta
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

def getKeyValue(d) :
	return str(d.day)+"_"+str(d.hour)+"_"+d.strftime("%M")


def getBurstiness(json):

	hist = {}
	dictTwHour = {}
	dictHourId = {}
	sumBin = {}
	mapTweetBin = {}
	res = {}

	dateMin = datetime.today()
	dateMax = datetime(2010,1,1)

	nbTweets = len(json)

	for doc in json :
		#pprint.pprint(doc)

		d = datetime.strptime(doc["created_at"], '%a %b %d %H:%M:%S %z %Y')
		print(d.strftime('%Y-%m-%d at %H:%M'))

		truncatedDate = datetime(year=d.year,month=d.month,day=d.day,hour=d.hour, minute=d.minute)

		if truncatedDate < dateMin :
			dateMin = truncatedDate
		if truncatedDate > dateMax :
			dateMax = truncatedDate

		key = getKeyValue(d)
		hist.setdefault(key,0)
		hist[key] += 1
		dictTwHour[doc["id_str"]] = key

	# Ici il faut combler les trous dans l'historique
	dCurrent = datetime(year=dateMin.year,month=dateMin.month,day=dateMin.day,hour=dateMin.hour, minute=dateMin.minute)
	while dCurrent < dateMax :
		k = getKeyValue(dCurrent)
		hist.setdefault(k,0)
		dCurrent += timedelta(minutes=1)


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


def getFreshness(json) :

	hist = {}
	res = {}

	dateMin = datetime.today()
	dateMax = datetime(2010,1,1)

	for doc in json :

		d = datetime.strptime(doc["created_at"], '%a %b %d %H:%M:%S %z %Y')
		print(d.strftime('%Y-%m-%d at %H:%M'))

		d2 = datetime(year=d.year, month=d.month, day=d.day, hour=d.hour, minute=d.minute, second=d.second)

		hist[doc["id_str"]] = d2

		if d2 < dateMin :
			dateMin = d2
		if d2 > dateMax :
			dateMax = d2

	print(dateMax - dateMin)
	delta = (dateMax - dateMin).total_seconds()

	for k in hist :
		res[k] = 1 - ( (dateMax - hist[k]).total_seconds() / delta )

	return res