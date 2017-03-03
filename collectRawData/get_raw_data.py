import pandas as pd
import json
import sys,os
import requests
import re
import socket
import urllib.request
from bs4 import BeautifulSoup

def isImg(f) :
	for ext in extensions_img :
		if f.endswith(ext) :
			return True
	return False


def extractDescription(soup):

	#print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

	og = soup.find("meta",  property="og:description")
	if og and og.has_attr("content") :
		#print(og)
		return og["content"]
	else :
		name = soup.find("meta", {"name":"description"})
		if name and name.has_attr("content"):
			return name["content"]
		else :
			og_title = soup.find("meta",  property="og:title")
			#print("og:title",og_title)
			if og_title and og_title.has_attr("content"):
				return og_title["content"]
			else :
				return soup.find("title").text


def getType(soup) :
	"""Permet de retrouver le type du lien en fonction de son contenu"""

	balise_type_lien = soup.find("meta", property="og:type")
	if balise_type_lien :
		type_lien = balise_type_lien["content"].lower()
		if "video" in type_lien:
			return "video"
		elif "photo" in type_lien :
			return "photo"
		elif "article" in type_lien :
			return "news"
		else :
			return "website"
	else :
		return "website"


def alreadyExtracted(eventId) :
	return os.path.exists("/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)+"/mapping/mapping.json")



DEBUG = False

if DEBUG :
	url = "http://m.mlb.com/video/?content_id=19899319&topic_id=&c_id=mlb&tcid=vpp_copy_19899319&v=3&partnerId=aw-8279914866082570605-1043"
	url = "https://www.instagram.com/p/BP-rXUGBPJa/?taken-by=beyonce&hl=en"
	req = requests.get(url, verify=False, timeout=5)

	s = BeautifulSoup(req.content, 'html.parser')
	balise_type_lien = s.find("meta", property="og:type")
	desc_lien = s.find("meta", property="og:description")
	image_lien = s.find("meta", property="og:image")

	print(balise_type_lien)
	print(desc_lien)
	print(image_lien)


	print(getType(s))

	print(extractDescription(s))

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



for eventId in listEventOk :

	if not alreadyExtracted(eventId) :

		set_tw = set()

#for eventId in [3] :
		mapping = {}
		id = 0
		inverse_mapping = {}

		# Création du répertoire pour chaque évènement
		dir_data = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)
		dir_urls = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)+"/urls/"
		dir_img = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)+"/images/"
		dir_videos = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)+"/videos/"
		dir_index = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)+"/to_index/"
		dir_mapping = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/" + str(eventId)+"/mapping/"
		os.system("rm -r "+dir_data)
		os.system("mkdir "+dir_data)
		os.system("mkdir " + dir_data+"/urls")
		os.system("mkdir " + dir_data+"/images")
		os.system("mkdir " + dir_data+"/videos")
		os.system("mkdir " + dir_data+"/to_index")
		os.system("mkdir " + dir_data+"/mapping")


		print("*********",eventId,"*********")
		# Lecture des fichiers json
		path_json = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/data_"+str(eventId)+".txt"
		f = open(path_json,"r")
		js = json.load(f)
		f.close()

		# Parcours des tweets pour chaque évènement
		for tw in js :

			if tw["id"] not in set_tw :

				set_tw.add(tw["id"])


				if "entities" in tw :

					id_tweet = str(tw["id"])

					text_tweet = tw["text"]
					text_tweet = re.sub(r"http\S+",'',text_tweet)

					# Si le texte n'est pas vide, on crée un enregistrement associé au tweet
					if id_tweet not in inverse_mapping :
						id = len(inverse_mapping)
						inverse_mapping[id_tweet] = id
						mapping[id] = {"origin":str(id_tweet), "type":"tweet", "tweets":[id_tweet],"description":text_tweet}


					# On s'occupe du champ media (les images uploadees)
					if "media" in tw["entities"] :
						for m in tw["entities"]["media"] :
							try:
								id_media = "upload_"+m["media_url"].split("/")[-1]
								origin = m["media_url"]
								urllib.request.urlretrieve(origin, dir_img+id_media)

								# Ajout dans la structure de mapping de l'image uploadee
								if id_media not in inverse_mapping:
									id = len(inverse_mapping)
									inverse_mapping[id_media] = id
									mapping[id] = {"origin": origin, "type": "img_upload", "tweets": [id_tweet], "description":text_tweet}
								else:
									mapping[inverse_mapping[id_media]]["tweets"].append(id_tweet)
									mapping[inverse_mapping[id_media]]["description"] += (" " + text_tweet)


							except urllib.error.HTTPError:
								print("404")


					# On s'occupe des entités (urls + images)
					if "urls" in tw["entities"] :
						for u in tw["entities"]["urls"] :
							url = u["expanded_url"]
							#print("************************************")
							print("\t",url)

							try :
								req = requests.get(url,verify=False, timeout=5)

								if req.status_code == 200 :
									id_media = req.url
									origin = req.url
									#print("\t", req.url)

									# Gestion image (le lien est directement une image) :
									if isImg(req.url) :
										try:
											id_media = req.url
											origin = req.url
											urllib.request.urlretrieve(req.url, dir_img + "remote_" + req.url.split("/")[-1])

											# Ajout dans la structure de mapping de l'image url
											if id_media not in inverse_mapping:
												id = len(inverse_mapping)
												inverse_mapping[id_media] = id
												mapping[id] = {"origin": origin, "type": "img_url", "tweets": [id_tweet], "description": text_tweet}
											else :
												mapping[inverse_mapping[id_media]]["tweets"].append(id_tweet)
												mapping[inverse_mapping[id_media]]["description"] += (" "+text_tweet)



										except urllib.error.HTTPError:
											print("404")
									else :

										content = req.content
										soup = BeautifulSoup(content, 'html.parser')

										if soup.find("title"):

											type_lien = getType(soup)

											if type_lien == "video" :
												# Une video ne pouvant pas être telechargée, on la décrit par son url et sa description
												desc = extractDescription(soup)
												print(desc)

												# Ajout dans la structure de mapping de l'image url
												if id_media not in inverse_mapping:
													id = len(inverse_mapping)
													inverse_mapping[id_media] = id
													mapping[id] = {"origin": origin, "type": "video", "tweets": [id_tweet], "description": text_tweet+" "+desc}
												else :
													mapping[inverse_mapping[id_media]]["tweets"].append(id_tweet)
													mapping[inverse_mapping[id_media]]["description"] += (" "+text_tweet)

											elif type_lien == "image" :
												origin = soup.find("meta", property="og:image")["content"]
												id_media = origin.split("/")[-1]
												urllib.request.urlretrieve(origin,dir_img + "html_" + id_media)
												desc = extractDescription(soup)

												# Ajout dans la structure de mapping de l'image "html"
												if id_media not in inverse_mapping:
													id = len(inverse_mapping)
													inverse_mapping[id_media] = id
													mapping[id] = {"origin": origin, "type": "img_html", "tweets": [id_tweet], "description": text_tweet+" "+desc}
												else :
													mapping[inverse_mapping[id_media]]["tweets"].append(id_tweet)
													mapping[inverse_mapping[id_media]]["description"] += (" "+text_tweet)


											elif type_lien == "news" :
												desc = extractDescription(soup)

												# on vire ce qu'il y a apres ? dans l'url
												id_media = id_media.split("?")[0]
												origin = origin.split("?")[0]


												# Ajout dans la structure de mapping de la news
												if id_media not in inverse_mapping:
													id = len(inverse_mapping)
													inverse_mapping[id_media] = id
													mapping[id] = {"origin": origin, "type": "news", "tweets": [id_tweet], "description": text_tweet+" "+desc}
												else :
													mapping[inverse_mapping[id_media]]["tweets"].append(id_tweet)
													mapping[inverse_mapping[id_media]]["description"] += (" "+text_tweet)


											else :
												#print(req.content)
												desc = extractDescription(soup)
												# on vire ce qu'il y a apres ? dans l'url
												id_media = id_media.split("?")[0]
												origin = origin.split("?")[0]
												# Ajout dans la structure de mapping de la news
												if id_media not in inverse_mapping:
													id = len(inverse_mapping)
													inverse_mapping[id_media] = id
													mapping[id] = {"origin": origin, "type": "website", "tweets": [id_tweet], "description": text_tweet+" "+desc}
												else :
													mapping[inverse_mapping[id_media]]["tweets"].append(id_tweet)
													mapping[inverse_mapping[id_media]]["description"] += (" "+text_tweet)


											desc_lien = soup.find("meta",  property="og:description")
											image_lien = soup.find("meta", property="og:image")

										#print("AFFICHAGE DES META")
										#print(type_lien)
										#print(desc_lien)
										#print(image_lien)
										#sys.exit()






								#print(req.content)
							except requests.exceptions.Timeout :
								print("\t\tsocket.timeout")
							except requests.exceptions.ConnectionError :
								print("\t\tsocket.gaierror")
							except requests.exceptions.ContentDecodingError :
								print("\t\tcontent.decoding.error")
							except requests.exceptions.TooManyRedirects :
								print("\t\trequests.exceptions.TooManyRedirects")

		for id in mapping :
			obj = mapping[id]
			if "tweet" in obj["type"]:
				with open(dir_index+"tweets.xml","a") as f :
					f.write("<DOC>\n<DOCNO>"+str(id)+"</DOCNO>\n"+obj["description"]+"\n</DOC>\n")
			elif "img" in obj["type"]:
				with open(dir_index+"images.xml","a") as f :
					f.write("<DOC>\n<DOCNO>"+str(id)+"</DOCNO>\n"+obj["description"]+"\n</DOC>\n")
			elif "video" in obj["type"]:
				with open(dir_index+"videos.xml","a") as f :
					f.write("<DOC>\n<DOCNO>"+str(id)+"</DOCNO>\n"+obj["description"]+"\n</DOC>\n")
			elif "news" in obj["type"]:
				with open(dir_index+"news.xml","a") as f :
					f.write("<DOC>\n<DOCNO>"+str(id)+"</DOCNO>\n"+obj["description"]+"\n</DOC>\n")
			elif "website" in obj["type"]:
				with open(dir_index+"websites.xml","a") as f :
					f.write("<DOC>\n<DOCNO>"+str(id)+"</DOCNO>\n"+obj["description"]+"\n</DOC>\n")

		json_file = dir_mapping+"mapping.json"
		with open(json_file, 'w') as outfile:
			json.dump(mapping, outfile)

		json_file = dir_mapping+"inverse.json"
		with open(json_file, 'w') as outfile:
			json.dump(inverse_mapping, outfile)


	#sys.exit()