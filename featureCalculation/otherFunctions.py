import pprint
import sys
from datetime import datetime
import pandas as pd

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

	return pd.DataFrame.from_dict(hist)
