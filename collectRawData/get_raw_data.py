import pandas as pd
import json
import sys,os
import requests
import socket
import urllib.request
from bs4 import BeautifulSoup

def isImg(f) :
	for ext in extensions_img :
		if f.endswith(ext) :
			return True
	return False


def extractDescription(soup):

	print("&&&&&&&&&&&&&&&&&&&")
	print(url)

	og = soup.find("meta",  property="og:description")
	if og :
		return og["content"]
	else :
		name = soup.find("meta", {"description":True})
		if name :
			return name["content"]
		else :
			og_title = soup.find("meta",  property="og:title")
			print("og:title",og_title)
			if og_title :
				return og_title["content"]
			else :
				return soup.find("title").contents[0]



DEBUG = True

if DEBUG :
	url = "http://m.mlb.com/video/?content_id=19899319&topic_id=&c_id=mlb&tcid=vpp_copy_19899319&v=3&partnerId=aw-8279914866082570605-1043"
	req = requests.get(url, verify=False, timeout=5)

	s = BeautifulSoup(req.content, 'html.parser')
	balise_type_lien = s.find("meta", property="og:type")
	desc_lien = s.find("meta", property="og:description")
	image_lien = s.find("meta", property="og:image")

	print(balise_type_lien)
	print(desc_lien)
	print(image_lien)

	sys.exit()




SEUIL = 100
csv_file = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/event_statistics.csv"

df = pd.read_csv(csv_file, sep="\t")
print(df)
gb = pd.DataFrame(df.groupby("IdEvent").sum().reset_index())

listEventOk = []

extensions_img = ["jpeg","jpg","exif","tiff","gif","bmp","png"]


for index, row in gb.iterrows() :
	if row["Tweets"] >= SEUIL :
		listEventOk.append(row["IdEvent"])

"""
try :
	urllib.request.urlretrieve('http://www.toto.fr/test.png', 'test.png')
except urllib.error.HTTPError :
	print("404")
sys.exit()


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

	# Création du répertoire pour chaque évènement
	dir_data = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)
	dir_urls = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)+"/urls/"
	dir_img = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)+"/images/"
	dir_videos = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)+"/videos/"
	os.system("rm -r "+dir_data)
	os.system("mkdir "+dir_data)
	os.system("mkdir " + dir_data+"/urls")
	os.system("mkdir " + dir_data+"/images")

	print("*********",eventId,"*********")
	# Lecture des fichiers json
	path_json = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/data_"+str(eventId)+".txt"
	f = open(path_json,"r")
	js = json.load(f)
	f.close()

	# Parcours des tweets pour chaque évènement
	for tw in js :
		if "entities" in tw :

			id_tweet = str(tw["id"])


			# On s'occupe du champ media (les images uploadees)
			if "media" in tw["entities"] :
				for m in tw["entities"]["media"] :
					try:
						urllib.request.urlretrieve(m["media_url"], dir_img+id_tweet+"_upload_"+m["media_url"].split("/")[-1])
					except urllib.error.HTTPError:
						print("404")

					sys.exit()

			# On s'occupe des entités (urls + images)
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

						# Gestion image :
						if isImg(req.url) :
							try:
								urllib.request.urlretrieve(req.url, dir_img + id_tweet + "_remote_" + req.url.split("/")[-1])
							except urllib.error.HTTPError:
								print("404")
						else :

							content = req.content
							soup = BeautifulSoup(content, 'html.parser')
							balise_type_lien = soup.find("meta",  property="og:type")
							type_lien = balise_type_lien["content"].lower()

							if "video" in type_lien :
								# Une video ne pouvant pas être telechargée, on la décrit par son url et sa description
								desc = extractDescription(soup)
								print(desc)
								sys.exit()



							desc_lien = soup.find("meta",  property="og:description")
							image_lien = soup.find("meta", property="og:image")

							print("AFFICHAGE DES META")
							print(type_lien)
							print(desc_lien)
							print(image_lien)
							sys.exit()


							mappingUrl.setdefault(req.url, [])
							mappingUrl[req.url].append(id_tweet)




						#print(req.content)
					except requests.exceptions.Timeout :
						print("socket.timeout")
					except requests.exceptions.ConnectionError :
						print("socket.gaierror")

	print(mappingUrl)
	sys.exit()