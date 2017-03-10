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

def getHistogram(json):

	hist = {}

	for doc in json :
		#pprint.pprint(doc)

		d = datetime.strptime(doc["created_at"], '%a %b %d %H:%M:%S %z %Y')
		print(d.strftime('%Y-%m-%d at %H:%M'))

		key = str(d.day)+"_"+str(d.hour)+"_"+d.strftime("%M")
		hist.setdefault(key,0)
		hist[key] += 1

	df = pd.DataFrame(columns=["id","time","count"])
	i = 0
	for k in sorted(hist):
		df.loc[i] = [i,k,hist[k]]
		i += 1

	# Bin the data frame by "a" with 10 bins...
	bins = np.linspace(df.id.min(), df.id.max(), 10)
	groups = df.groupby(np.digitize(df.id, bins))

	print(bins)
	print(groups.sum())

	return df
