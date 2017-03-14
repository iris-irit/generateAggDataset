import os, sys
import json
import tweepy

from socialFunctions import *









config = {}
config["consumer_key"] = "SCeH2iu0A9IeDie3v37yilzan"
config["consumer_secret"] = "lifjtDGi2Okzx9FEyDJLTWQsdNGmKPlWAZPgMeUyENcETHwTS7"
config["access_key"] = "831848639916027904-lAPXqf5MQNo33Ar36eQbPcapMuKlQxd"
config["access_secret"] = "QvCQuTZmpE8zhWoNmvXmYW8k1ytz0BinVRgbvDHsvkxow"


#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------

auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])
auth.set_access_token(config["access_key"], config["access_secret"])

api = tweepy.API(auth, wait_on_rate_limit=True,retry_errors=131,retry_count=2)





path_events = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Raw/"
path_json =  "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Preliminaries/"
path_features = "/projets/iris/PROJETS/PRINCESS/TournAgg/Datasets/Features/"


name_dir_mapping = "/mapping/mapping.json"
name_dir_inverse = "/mapping/inverse.json"

features = {}
mappingDocTweets = {}
mappingTweetUser = {}
userActivity = {}

for repEvent in os.listdir(path_events) :

	if not os.path.exists(path_features+repEvent) :
		os.mkdir(path_features+repEvent)

	with open(path_json+"data_"+repEvent+".txt", "r") as fjson :
		json_raw = json.load(fjson)

	with open(path_events+repEvent+name_dir_mapping, "r") as fjson :
		mapping = json.load(fjson)

	with open(path_events+repEvent+name_dir_inverse, "r") as fjson :
		inverse = json.load(fjson)


	# Pour chaque document dans la collection, on cherche les utilisateurs des tweets associés à ce document
	for idDoc in mapping :

		mappingDocTweets[idDoc] = mapping[idDoc]["tweets"]

		for tw in mapping[idDoc]["tweets"] :

			if tw not in mappingTweetUser :
				data = lookupTweet(int(tw), json_raw)
				mappingTweetUser[tw] = data['user']['id']

	# Pour chaque tweet concerné par l'évènement, on recherche l'activité de l'utilisateur (en évitant de réinterroger si
	# on a déjà croisé cet utilisateur

	for tw in mappingTweetUser :

		if mappingTweetUser[tw] not in userActivity :  # si on n'a pas croisé l'utlisateur
			user = api.get_user(user_id=mappingTweetUser[tw])
			print(user["_json"]["status"])

			sys.exit(0)





	with open(path_features+repEvent+"/social.json", "w") as fout :
		json.dump(features,fout)