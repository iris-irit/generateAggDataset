import pprint
import sys
from datetime import datetime

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
		print(d.strftime('%Y-%m-%d at %H'))

		key = str(d.day)+"_"+str(d.hour)+"_"+str(d.minute)
		hist.setdefault(key,0)
		hist[key] += 1

	return sorted(hist.items())
