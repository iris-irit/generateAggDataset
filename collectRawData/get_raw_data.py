import pandas as pd
import json
import sys
import requests
import socket
import urllib.request



SEUIL = 100
csv_file = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/event_statistics.csv"

df = pd.read_csv(csv_file)
gb = pd.DataFrame(df.groupby("IdEvent").sum().reset_index())

listEventOk = []

for index, row in gb.iterrows() :
	if row["Tweets"] >= SEUIL :
		listEventOk.append(row["IdEvent"])

try :
	urllib.request.urlretrieve('http://www.toto.fr/test.png', 'test.png')
except urllib.error.HTTPError :
	print("404")
sys.exit()

"""
url404 = "https://twitter.com/WheresKernan/status/256925517494763520"
req = requests.get(url404,verify=False, timeout=5)
print(req.status_code)
print(req.history)
with open("test.html","w") as f : 
	f.write(req.content.decode('utf-8'))

sys.exit()
"""



#for eventId in listEventOk :
for eventId in [3] :
	mappingUrl = {}
	print("*********",eventId,"*********")
	path_json = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/data_"+str(eventId)+".txt"
	f = open(path_json,"r")
	js = json.load(f)

	#print(js)
	f.close()
	
	for tw in js : 
		if "entities" in tw :

			if "media" in tw["entities"] : 
				for m in tw["entities"]["media"] :
					print(m)
					urllib.request.urlretrieve(m["media_url"], m["media_url"].split("/")[-1])

					sys.exit()

			if "urls" in tw["entities"] :
				for u in tw["entities"]["urls"] :
					url = u["expanded_url"]
					print("************************************")
					print(url)
					try :
						req = requests.get(url,verify=False, timeout=5)
						
						if req.status_code == 404 :
							print("404")
						print(req.status_code)
						print(req.url)

						mappingUrl.setdefault(req.url, 0)
						mappingUrl[req.url] += 1
						#print(req.content)
					except requests.exceptions.Timeout :
						print("socket.timeout")
					except requests.exceptions.ConnectionError :
						print("socket.gaierror")

	print(mappingUrl)
	sys.exit()